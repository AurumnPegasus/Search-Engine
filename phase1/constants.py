BODY_THRESHOLD = 7

INFOBOX_ID = '{{Infobox '
INFOBOX_END_ID = '}}'

REF_ID = 'References'

LINK_ID = 'External links'
LINK_2_ID = 'Other links'

CAT_ID = '[[Category:'
CAT_END_ID = ']]'

END_ID = '=='

INFO_FLAG = 'infobox'
BODY_FLAG = 'body'
CAT_FLAG = 'category'
LINK_FLAG = 'links'
REF_FLAG = 'references'

REGEX = r'('

# Scheme (HTTP, HTTPS):
REGEX += r'(?:(https?):\/\/)?'

# www:
REGEX += r'(?:www\.)?'

REGEX += r')'

MAX_CACHE = 250000

LOW_THRESHOLD = 2
HIGH_THRESHOLD = 14

FIELD_Q = {
    't',
    'b',
    'i',
    'r',
    'c',
    'l'
}

FIELD_WEIGHTS = {
    't': 5,
    'b': 1,
    'i': 4,
    'r': 2,
    'c': 3,
    'l': 2
}

MATCH_SCORE = 7

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
    'wikipedia'
]

FIELDS = {
    'title': 0,
    'body': 1,
    'infobox': 2,
    'references': 3,
    'category': 4,
    'links': 5
}

IMP_THRESHOLD = 1
WORD_DELIM = '*'
DOC_DELIM = ';'
