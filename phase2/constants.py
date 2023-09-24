# Flags
BODY = 'body'
INFO = 'infobox'
CAT = 'category'
LINK = 'links'
REF = 'references'
B = 'b'
I = 'i'
C = 'c'
L = 'l'
R = 'r'
T = 't'

# Start/End of Events
INFOBOX_ID = '{{Infobox '
L_INFOBOX_ID = 10

REF_ID = 'References'
L_REF_ID = 10

LINK_ID = 'External links'
LINK_2_ID = 'Other links'
CAT_ID = '[[Category:'

END_1 = '}}'
END_2 = ']]'
END_3 = '=='
L_END = 2

# Tokenization
LOW_THRESHOLD = 1
HIGH_THRESHOLD = 11
NUM_HIGH_THRESHOLD = 8
NA_HIGH_THRESHOLD = 4
ADDED_STOPWORDS = [
    'references',
    'reflist',
    'category',
    'infobox',
    'wiki',
    'image',
    'http',
    'https',
    'com',
    'www',
    'wikiproject',
    'wikipedia',
    'the'
]
MAX_CACHE = 100000
DICSIZE = 500000
HEAPSIZE = 500000

WORDS = ';'
DOCS = '*'
INV = '\n'

# Search
WEIGHTS = {
    'b': 5,
    'c': 50,
    'i': 30,
    'l': 5,
    'r': 5,
    't': 100
}
MATCH = 100
BMATCH = 10
