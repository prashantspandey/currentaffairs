from more_itertools import unique_everseen
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from sklearn.cluster import KMeans
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import defaultdict
from string import punctuation
from heapq import nlargest
from nltk import pos_tag
import nltk
import json
import datetime
import pickle

def read_file(path):
    with open(path,'rb') as fi:
        content_list = pickle.load(fi)
    return content_list

def find_pos(content):
    if type(content) == list:
        cont = ','.join(content)
    else:
        cont = content
    _stopwords = set(stopwords.words('english') + list(punctuation))
    token = word_tokenize(cont)
    #find_bigrams(token)
    words = []
    for i in token:
        if i not in _stopwords and i != '’' and i != '”':
            words.append(i)
    find_nnp(words)


def find_nnp(words):
    tagged = pos_tag(words)
    noun_tags = []
    for i,j in tagged:
        if j == 'NNP':
            noun_tags.append(i)
            print(words.index(i))
    counts = Counter(noun_tags)
    print(noun_tags)
#def find_bigrams(words):
#    bigram = list(nltk.bigrams(words))
#    _stopwords = set(stopwords.words('english') + list(punctuation))
#    for i,j in bigram:
#        if i not in _stopwords and i != '’' and i != '”':
#
#        joined = str(i) + ' '+  str(j)
#        print(joined)
#        find_nnp(str(joined))

#if __name__ == '__main__':
#    content_list = read_file('hindu_content.pickle')
#    for num,content in enumerate(content_list):
#        if num == 1:
#            paras = content['paragraphs']
#            find_pos(paras)
#            try:
#                date = content['description']
#                #print(date)
#            except Exception as e:
#                print(str(e))
#            #find_pos(paras)
#    print(len(content_list))
