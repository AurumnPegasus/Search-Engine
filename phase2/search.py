import imports as im

if __name__ == "__main__":
    start = im.time.time()
    # Getting all the queries
    queryfile = im.sys.argv[1]
    with open(queryfile) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    # Loading all the files of inverted index
    index_path = im.sys.argv[2]
    invindexfiles = list(im.os.listdir(index_path))
    invindexfiles = im.natsorted(invindexfiles)
    invindexfiles = invindexfiles[:-3]
    titlefiles = list(im.os.listdir(f'{index_path}titles/'))
    titlefiles = im.natsorted(titlefiles)
    # tcounts = [int(im.os.popen(f'tail -1 {index_path}titles/{titfile}').read().strip().split()[0]) for titfile in titlefiles]
    numdocs = int(im.os.popen(f'tail -1 {index_path}titles/{invindexfiles[-1]}').read().strip().split()[0])

    lwpath = f'{index_path}lastword.txt'
    with open(lwpath) as f:
        lastwords = f.readlines()
        lastwords, lwpageid = [line.split()[0].strip() for line in lastwords], [line.split()[1].strip() for line in lastwords]

    twpath = f'{index_path}lasttitle.txt'
    with open(twpath) as f:
        titlewords = f.readlines()
        tcounts = [int(line.split()[0].strip()) for line in titlewords]

    lower = str.lower

    # Going through all queries
    for query in lines:
        tokens = tags = []
        word = ""
        append = tokens.append
        cstart = im.time.time()

        # Tokenizing query
        for c in query:
            if c in im.CHARSET or c == ':':
                word = f'{word}{c}'
            elif len(word) > im.LOW_THRESHOLD and len(word) < im.HIGH_THRESHOLD and word not in im.STOPWORDS:
                append(lower(word))
                word = ""
            else:
                word = ""

        # final word
        if len(word) > im.LOW_THRESHOLD and len(word) < im.HIGH_THRESHOLD and word not in im.STOPWORDS:
            append(lower(word))
        scores = im.defaultdict(float)

        # Going through all words in query
        for token in tokens:

            # Finding token v tag
            tag = None
            if token[1] == ':':
                tag, token = token[0], token[2:]

            # Finding the file of inv index of the query
            idx = im.bisect_left(lastwords, token)
            pid = lwpageid[idx]
            fp = open(f'{index_path}{pid}.txt', 'r')

            # Reading each line in the file
            line = fp.readline()

            # Reading each line
            while line != '':

                # If I found what I wanted
                if line.startswith(f'{token}{im.DOCS}'):
                    docs = line.split(im.DOCS)[1:]
                    idf = im.math.log((1 + numdocs)/(1 + len(docs)))

                    # Going through all docs word occurs in
                    for doc in docs:
                        value = ''
                        isdocid = False
                        docid = ''
                        tf = 0

                        # Going through each letter of doc repr
                        for text in doc:
                            if text.isalpha():
                                if not isdocid:
                                    docid = value
                                    isdocid = True
                                else:
                                    if value =='':
                                        value = '1'
                                    value = int(value)
                                    if tag is not None:
                                        if tag == 'b':
                                            tf += im.math.log(1 + im.BMATCH*im.WEIGHTS[text]*value)
                                        else:
                                            tf += im.math.log(1 + im.MATCH*im.WEIGHTS[text]*value)
                                    else:
                                        tf += im.math.log(1 + im.WEIGHTS[text]*value)
                                value = ''
                            else:
                                value += text

                        # Calculating TF IDF for a document
                        tfidf = tf*idf
                        scores[docid] += tfidf
                    break
                else:
                    line = fp.readline()

        # Calculating scores of tf idf of all tokens across all docs
        lscores = im.nlargest(10, scores, key=scores.__getitem__)
        ds = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        if len(lscores) < 10:
            lscores.extend(ds[:(10 - len(lscores))])
        fout = open('queries_op.txt', 'a')
        for docid in lscores:
            idx = im.bisect_left(tcounts, int(docid))
            ftp = open(f'{index_path}titles/{idx}.txt')
            title = ftp.readline().strip()
            while title:
                td = title.split()
                if td[0] == docid:
                    im.ic(td[0], ' '.join(td[1:]))
                    fout.write(f"{td[0]} {' '.join(td[1:])}\n")
                    break
                else:
                    title = ftp.readline().strip()
        fout.write(f'TIME: {im.time.time() - cstart}\n')
        fout.write('\n')
    fout.close()
    im.ic(im.time.time() - start)
