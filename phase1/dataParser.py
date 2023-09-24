import imports as im

def tokenizeText(text):
    word = ""

    # tokenize the words
    tokens = []
    for c in text:
        if c.isalnum():
            word += c
        elif len(word) > im.LOW_THRESHOLD and len(word) < im.HIGH_THRESHOLD and word not in im.STOPWORDS:
            tokens.append(word.lower())
            word = ""
        else:
            word = ""
    num = len(tokens)
    # stemming the words
    tokens = im.STEMMER.stemWords(tokens)

    # finding counts of words
    counts = {}
    for i in tokens:
        counts[i] = counts.get(i, 0) + 1
    return counts, num
