import imports as im

class Search:
    def __init__(self, index_path, query_string):
        self.index_path = index_path
        self.query_string = query_string
        self.index = {}
        self.i2d = {}

    def loadIndex(self):
        f = open(f'{self.index_path}inverted_index.txt', 'r')
        index_string = f.read()
        indices = index_string.split(im.WORD_DELIM)
        for ind in indices:
            tokens = ind.split(im.DOC_DELIM)
            word = tokens[0]
            self.index[word] = [tokens[1:]]

        f = open(f'{self.index_path}page2title.txt', 'r')
        i2d = f.read()
        i2d = i2d.split(im.WORD_DELIM)
        for i in i2d:
            q = i.split(im.DOC_DELIM)
            if len(q) != 2:
                continue
            key, value = q[0], q[1]
            self.i2d[key] = value

    def processQuery(self):
        tokens = self.query_string.split()
        self.query_words = {}
        till_now = []
        prev_q = 'b'
        for tok in tokens:
            if tok == ':':
                continue
            if tok in im.FIELD_Q:
                self.query_words[prev_q] = till_now
                till_now = []
                prev_q = tok
            else:
                till_now.append(tok)
        self.query_words[prev_q] = till_now

    def scoreDocs(self, doc):
        score = 0
        nw = 0
        pageid = 0
        prev = doc[0]
        for c in doc:
            if c in im.FIELD_Q or c == 'd':
                score += nw*im.FIELD_WEIGHTS[prev]
                prev = c
                nw = 0
            else:
                nw = 10*nw + int(c)
        return score, str(nw)

    def getResults(self):
        possible_results = []
        for key, value in self.query_words.items():
            for word in value:
                if word not in self.index:
                    continue

                docs = self.index[word]
                for doc in docs[0]:
                    possible_results.append(self.scoreDocs(doc))

        sorted(possible_results)
        for i in possible_results[:10]:
            im.ic(self.i2d[i[1]])


if __name__ == "__main__":
    index_path = im.sys.argv[1]
    query_string = im.sys.argv[2]
    s = Search(index_path, query_string)
    s.loadIndex()
    s.processQuery()
    s.getResults()
