from ctypes.wintypes import tagMSG
import imports as im

class DataHandler(im.sax.ContentHandler):
    def __init__(self, index_path):
        self.current_data = ""
        self.index_path = index_path

        # Creating object of Page
        self.page = None
        self.page_id = 0

        # Data Reading
        self.flags = {
            im.BODY: True,
            im.INFO: False,
            im.CAT: False,
            im.LINK: False,
            im.REF: False
        }
        self.keys = self.flags.keys()

        # Page specific data
        self.title = ""
        self.body = []

        # Temporary disk write
        self.disk_path = "/scratch/shivansh.s/temp/"
        self.count = 0
        self.items = []
        self.titems = []

        self.t = im.time.time()

    def setFlag(self, toTrue):
        for k in self.keys:
            if self.flags[k]:
                self.flags[k] = False
                break
        self.flags[toTrue] = True

    def startEvent(self, line):
        if not self.flags[im.INFO] and line[:im.L_INFOBOX_ID] == im.INFOBOX_ID:
            self.setFlag(im.INFO)
        elif not self.flags[im.REF] and line[:im.L_END] == im.END_3 and line[-im.L_END:] == im.END_3 and im.REF_ID == line[im.L_END: -im.L_END].strip():
            self.setFlag(im.REF)
        elif not self.flags[im.CAT] and line[:im.L_END] == im.CAT_ID:
            self.setFlag(im.CAT)
        elif not self.flags[im.LINK] and line[:im.L_END] == im.END_3 and line[-im.L_END:] == im.END_3 and (im.LINK_ID == line[im.L_END: -im.L_END].strip() or im.LINK_2_ID == line[im.L_END: -im.L_END].strip()):
            self.setFlag(im.LINK)

    def endEvent(self, line):
        if self.flags[im.INFO] and line[-im.L_END :] == im.END_1 and line[-im.L_END :] != im.END_1:
            if line.find("{{"):
                self.setFlag(im.BODY)
        elif line[: im.L_END] == im.END_3 and line[-im.L_END :] == im.END_3:
            self.setFlag(im.BODY)
        elif line[-im.L_END :] == im.END_2 and self.flags[im.CAT]:
            self.setFlag(im.BODY)

    def startElement(self, name, attrs):
        self.current_data = name
        if name == 'page':
            self.setFlag(im.BODY)
            self.page = im.Page(self.page_id)

    def endElement(self, name):
        if self.current_data == "text":
            for line in self.body:
                self.endEvent(line)
                self.startEvent(line)

                if self.flags[im.BODY]:
                    self.page.addLine(line)
                elif self.flags[im.INFO]:
                    self.page.addInfoBox(line)
                elif self.flags[im.REF]:
                    self.page.addRefs(line)
                elif self.flags[im.CAT]:
                    self.page.addCategory(line)
                elif self.flags[im.LINK]:
                    self.page.addLinks(line)
            self.body = []
        elif self.current_data == "title":
            self.page.addTitle(self.title)
            self.title = ""
        elif name == "page":
            self.titems.append([self.page_id, self.page.title.strip()])
            self.items.extend(self.page.tokenizeText(self.page.title, im.T))
            self.items.extend(self.page.tokenizeText(self.page.body, im.B))
            if len(self.items) > im.DICSIZE:
                self.hardWrite()
            self.items.extend(self.page.tokenizeText(self.page.infobox, im.I))
            self.items.extend(self.page.tokenizeText(self.page.category, im.C))
            self.items.extend(self.page.tokenizeText(self.page.links, im.L))
            self.items.extend(self.page.tokenizeText(self.page.refs, im.R))
            if len(self.items) > im.DICSIZE:
                self.hardWrite()
            self.page_id += 1
            if self.page_id%10000 == 0:
                im.ic(self.page_id, im.time.time() - self.t)

    def characters(self, content):
        if self.current_data == "text":
            self.body.append(content)
        elif self.current_data == "title":
            self.title = f'{self.title}{content}'

    def hardWrite(self):
        path = f'{self.disk_path}{self.count}.txt'
        self.items.sort()
        with open(path, 'w') as f:
            for item in self.items:
                f.write(f'{item}\n')
        self.items = []
        pathB = f'{self.index_path}titles/{self.count}.txt'
        self.count += 1
        with open(pathB, 'w') as f:
            for id, title in self.titems:
                f.write(f'{id} {title}\n')
        self.titems = []

if __name__ == "__main__":
    data_path = im.sys.argv[1]
    index_path = im.sys.argv[2]
    index_stat_path = im.sys.argv[3]
    parser = im.sax.make_parser()
    parser.setFeature(im.sax.handler.feature_namespaces, 0)
    Handler = DataHandler(index_path)
    parser.setContentHandler(Handler)
    pages = parser.parse(data_path)
    Handler.hardWrite()
