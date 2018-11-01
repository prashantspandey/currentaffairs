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
    print('got into find_pos')
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
    keywords = find_nnp(words)
    print('return keyword')
    return keywords


def find_nnp(words):
    print('in find_nnp')
    tagged = pos_tag(words)
    noun_tags = []
    noun_index = []
    for i,j in tagged:
        if j == 'NNP':
            noun_tags.append(i)
            noun_index.append(words.index(i))
    final_keys = []
    for num,nind in enumerate(noun_index):
        if nind > 0:
            try:
                if noun_index[nind+1] - noun_index[nind] == 1:
                    key1 = noun_index[nind]
                    key2 = noun_index[nind+1]
                    long_key = str(words[key1])+' '+ str(words[key2])
                    nind = nind+2
                    print('old key1  {}'.format(key1))
                    print('old key2 {}'.format(key2))
                    print('long key {}'.format(long_key))
                    print('new nind {}'.format(nind))
                    final_keys.append(long_key)
                else:
                    final_keys.append(words[num])
            except Exception as e:
                print(str(e))
    print(final_keys)
    return final_keys

        

   
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
