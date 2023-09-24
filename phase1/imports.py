from icecream import ic
import xml.sax as sax
from page import Page
import re
from constants import *
from dataParser import *
import time
from collections import defaultdict
from nltk.corpus import stopwords
import Stemmer
import sys

STEMMER = Stemmer.Stemmer('english')
URLS = re.compile(REGEX, re.IGNORECASE)
STEMMER.maxCacheSize = MAX_CACHE
STOPWORDS = set(stopwords.words('english') + ADDED_STOPWORDS)
