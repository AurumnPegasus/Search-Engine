import imports as im

class Page:
    def __init__(self, page_id):
        self.page_id = page_id
        self.title = ""
        self.body = ""
        self.infobox = ""
        self.refs = ""
        self.category = ""
        self.links = ""

    def addTitle(self, line):
        self.title = line

    def addLine(self, line):
        self.body = f'{self.body} {line}'

    def addLinks(self, line):
        self.lins = f'{self.links} {line}'

    def addInfoBox(self, line):
        if line[0] == '|':
            line = line[1:]
        sep = line.find('=')
        if sep != -1:
            value = line[sep+1:]
            if len(value) > 0:
                self.infobox = f'{self.infobox} {line}'

    def addRefs(self, line):
        self.refs = f'{self.refs} {line}'

    def addCategory(self, line):
        self.category = f'{self.category} {line}'

    def tokenizeText(self, text, tag):
        word = ""
        tokens = []
        tags = []

        lower = str.lower
        append1 = tokens.append
        append2 = tags.append
        for c in text:
            if c in im.CHARSET:
                word = f'{word}{c}'
            elif len(word) > im.LOW_THRESHOLD and len(word) < im.HIGH_THRESHOLD and word not in im.STOPWORDS:
                if word.isnumeric() and len(word) > im.NUM_HIGH_THRESHOLD:
                    word = ""
                elif not word.isalpha() and not word.isnumeric() and len(word) > im.NA_HIGH_THRESHOLD:
                    word = ""
                else:
                    append1(lower(word))
                    append2(tag)
                    word = ""
            else:
                word = ""

        tokens = im.STEMMER.stemWords(tokens)
        tokens = [f'{i} {self.page_id} {j}' for i, j in zip(tokens, tags)]
        return tokens

    def __repr__(self) -> str:
        return 'page_id: ' + str(self.page_id) + \
                ' body: ' + str(self.body) + \
                ' infobox: ' + str(self.infobox) + \
                ' links: ' + str(self.links) + \
                ' references: ' + str(self.references) + \
                ' categories: ' + str(self.category)
