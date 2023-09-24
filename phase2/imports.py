from icecream import ic
import xml.sax as sax
from constants import *
from page import Page
import time
import sys
import os
from nltk.corpus import stopwords
import Stemmer
from heapq import heappop, heappush, heapify, nlargest
from natsort import natsorted
from bisect import bisect_left
import math
from collections import defaultdict
import string

STOPWORDS = set(stopwords.words('english') + ADDED_STOPWORDS)
STEMMER = Stemmer.Stemmer('english')
STEMMER.maxCacheSize = MAX_CACHE
CHARSET = string.ascii_letters + string.digits

