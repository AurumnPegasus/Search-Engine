import imports as im

class DataHandler(im.sax.ContentHandler):
    def __init__(self):
        self.current_data = ""
        self.page = None
        self.page_id = 0
        self.info_id = None
        self.flags = {
            'body': True,
            'infobox': False,
            'category': False,
            'links': False,
            'references': False
        }
        self.title = []
        self.body = []
        self.t = im.time.time()
        self.inverted_index = {}
        self.pages_titles = {}
        self.vocab = 0
        self.bvocab = 0

    def setFlag(self, key):
        for k in self.flags.keys():
            if k == key:
                self.flags[k] = True
            else:
                self.flags[k] = False

    def startEvent(self, line):
        if not self.flags[im.INFO_FLAG] and line[:len(im.INFOBOX_ID)] == im.INFOBOX_ID:
            self.setFlag(im.INFO_FLAG)
        elif not self.flags[im.REF_FLAG] and line[:len(im.END_ID)] == im.END_ID and line[-len(im.END_ID):] == im.END_ID and im.REF_ID == line[len(im.END_ID): -len(im.END_ID)].strip():
            self.setFlag(im.REF_FLAG)
        elif not self.flags[im.CAT_FLAG] and line[:len(im.CAT_ID)] == im.CAT_ID:
            self.setFlag(im.CAT_FLAG)
        elif not self.flags[im.LINK_FLAG] and line[:len(im.END_ID)] == im.END_ID and line[-len(im.END_ID):] == im.END_ID and (im.LINK_ID == line[len(im.END_ID): -len(im.END_ID)].strip() or im.LINK_2_ID == line[len(im.END_ID): -len(im.END_ID)].strip()):
            self.setFlag(im.LINK_FLAG)

    def endEvent(self, line):
        if self.flags[im.INFO_FLAG] and (line[-len(im.INFOBOX_END_ID):] == im.INFOBOX_END_ID and \
                        not (line[-len(im.INFOBOX_END_ID):] == im.INFOBOX_END_ID)):
            if line.find("{{"):
                self.setFlag(im.BODY_FLAG)
        elif line[:2] == im.END_ID and line[-2:] == im.END_ID:
            self.setFlag(im.BODY_FLAG)
        elif line[-2:] == im.CAT_END_ID and self.flags[im.CAT_FLAG]:
            self.setFlag(im.BODY_FLAG)

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == "page":
            self.setFlag(im.BODY_FLAG)
            self.page = im.Page(self.page_id)

    def endElement(self, tag):
        if self.current_data == "text":
            for line in self.body:
                self.endEvent(line)
                self.startEvent(line)

                # If parsing Links
                if self.flags[im.LINK_FLAG]:
                    self.page.addLinks(line)

                # If parsing Infobox text
                if self.flags[im.INFO_FLAG]:
                    self.page.addInfoBox(line)

                # If parsing References
                if self.flags[im.REF_FLAG]:
                    self.page.addReferences(line)

                # If parsing categories
                if self.flags[im.CAT_FLAG]:
                    self.page.addCategory(line)

                # Normal text parsing
                if self.flags[im.BODY_FLAG]:
                    self.page.addLine(line)
            self.body = []
        elif self.current_data == "title":
            self.page.addTitle(' '.join(self.title))
            self.title = []
        elif tag == "page":
            self.page.tokenizeEverything()
            self.pages_titles[self.page_id] = str(self.page_id) + ';' + self.page.title
            dval = self.page.page_id
            self.bvocab += self.page.before_stem
            # self.vocab += len(self.page.unique)
            for word in self.page.unique:
                tval = self.page.tit.get(word, 0)
                bval = self.page.body.get(word, 0)
                ival = self.page.infobox.get(word, 0)
                rval = self.page.references.get(word, 0)
                cval = self.page.category.get(word, 0)
                lval = self.page.links.get(word, 0)

                current = ""
                if tval + bval + ival + rval + cval + lval <= im.IMP_THRESHOLD:
                    continue
                if tval > 0:
                    current += 't' + str(tval)
                if bval > 0:
                    current += 'b' + str(bval)
                if ival > 0:
                    current += 'i' + str(ival)
                if rval > 0:
                    current += 'r' + str(rval)
                if cval > 0:
                    current += 'c' + str(cval)
                if lval > 0:
                    current += 'l' + str(lval)
                current += 'd' + str(dval)
                if word in self.inverted_index:
                    self.inverted_index[word] += ';' + current
                else:
                    self.inverted_index[word] = word + ';' + current
            self.page_id += 1
            if self.page_id%10000 == 0:
                im.ic(self.page_id, im.time.time() - self.t)
        self.current_data = ""

    def characters(self, content):
        if self.current_data == "text":
            if len(content) > im.BODY_THRESHOLD:
                self.body.append(content)
        elif self.current_data == "title":
            self.title.append(content)

if __name__ == "__main__":

    parser = im.sax.make_parser()
    parser.setFeature(im.sax.handler.feature_namespaces, 0)
    Handler = DataHandler()
    parser.setContentHandler(Handler)
    data_path = im.sys.argv[1]
    index_path = im.sys.argv[2]
    index_stat_path = im.sys.argv[3]
    pages = parser.parse(data_path)
    # parser.parse('../subset.xml')

    ii = open(f'{index_path}inverted_index.txt', 'w')
    ii.write('*'.join(list(Handler.inverted_index.values())))
    ii.close()
    im.ic(im.time.time() - Handler.t)

    id2t = open(f'{index_path}page2title.txt', 'w')
    id2t.write('*'.join(list(Handler.pages_titles.values())))
    id2t.close()

    f = open(f'{index_stat_path}', 'w')
    f.write(str(Handler.bvocab))
    f.write('\n')
    f.write(str(len(Handler.inverted_index.keys())))
    f.close()
    im.ic(im.time.time() - Handler.t)
