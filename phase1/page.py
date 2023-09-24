import imports as im

class Page:
    def __init__(self, page_id):
        self.page_id = page_id
        self.title = ""
        self.body = ""
        self.infobox = ""
        self.references = ""
        self.category = ""
        self.links = ""
        self.unique = set()

    def addTitle(self, line):
        self.title = line

    def addLine(self, line):
        self.body += ' ' + line

    def addLinks(self, line):
        self.links += ' ' + line

    def addInfoBox(self, line):
        if line[0] == '|':
            line = line[1:]
        sep = line.find('=')
        if sep != -1:
            value = line[sep + 1:]
            if len(value) > 0:
                self.infobox += ' ' + value

    def addReferences(self, line):
        self.references += ' ' + line

    def addCategory(self, line):
        if line[:len(im.CAT_ID)] == im.CAT_ID:
            line = line[len(im.CAT_ID):-len(im.CAT_END_ID)]
        self.category += ' ' + line

    def tokenizeEverything(self):
        total_num = 0
        if len(self.body) > 0:
            self.body, num = im.tokenizeText(self.body)
            total_num += num
        else:
            self.body = {}
        if len(self.infobox) > 0:
            self.infobox, num = im.tokenizeText(self.infobox)
            total_num += num
        else:
            self.infobox = {}
        if len(self.references) > 0:
            self.references, num = im.tokenizeText(self.references)
            total_num += num
        else:
            self.references = {}
        if len(self.category) > 0:
            self.category, num = im.tokenizeText(self.category)
            total_num += num
        else:
            self.category = {}
        if len(self.links) > 0:
            self.links, num = im.tokenizeText(self.links)
            total_num += num
        else:
            self.links = {}
        if len(self.title) > 0:
            self.tit, num = im.tokenizeText(self.title)
            total_num += num
        else:
            self.tit = {}

        total_dict = self.body | self.infobox | self.references | self.category | self.links | self.tit
        self.unique = total_dict.keys()
        self.before_stem = total_num

    def __repr__(self) -> str:
        return 'page_id: ' + str(self.page_id) + \
                ' body: ' + str(self.body) + \
                ' infobox: ' + str(self.infobox) + \
                ' links: ' + str(self.links) + \
                ' references: ' + str(self.references) + \
                ' categories: ' + str(self.category)

if __name__ == "__main__":
    pass
