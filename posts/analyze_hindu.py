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
import requests
url =\
"https://language.googleapis.com/v1/documents:analyzeEntities?key=AIzaSyDOW6Nt-1jpzxcEbypSpJ-ObCsZHjYBjPA"

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

    #_stopwords = set(stopwords.words('english') + list(punctuation))
    #token = word_tokenize(cont.lower())
    #find_bigrams(token)
    #words = []
    #for i in token:
    #    if i not in _stopwords and i != '’' and i != '”':
    #        words.append(i)
    text ={"document":{"content":cont.lower(),"type":"PLAIN_TEXT"}}
    r = requests.post(url,json=text)
    data = r.text
    #type_name = data['name']
    #type_type = data['type']
    #type_mentions_type = data['mentions']['type']
    #type_wikipedia = data['metadata']['wikipedia_url']
    json_data = json.loads(data)
    print(len(json_data['entities']))
    final_keywords =[]
    for i in range(len(json_data['entities'])):
        name = json_data['entities'][i]['name']
        type_entity = json_data['entities'][i]['type']
        try:
            type_wikipedia = json_data['entities'][i]['metadata']['wikipedia_url']
        except:
            type_wikipedia = None
        type_nnp = json_data['entities'][i]['mentions'][0]['type']
        print(name)
        print(type_entity)
        print(type_wikipedia)
        print(type_nnp)
        keys =\
                {'name':name,'entity':type_entity,'wikipedia':type_wikipedia,'type_nnp':type_nnp}
        final_keywords.append(keys)


            

        #print(type_type)
        #print(type_mentions_type)
        #print(type_wikipedia)
    #keywords = find_nnp(token)
    #if keywords:
    #    keywords = list(unique_everseen(keywords))
    return final_keywords


def find_nnp(words):
    print('in find_nnp')
    tagged = pos_tag(words)
    noun_tags = []
    noun_index = []
    for i,j in tagged:
        if j == 'NNP':
            noun_tags.append(i)
            noun_index.append(words.index(i))
            print('This is the live keyword {}'.format(i))
    if len(noun_tags) !=0:
        final_keys = []
        index_tag = 0
        for tag in range(len(noun_index)):
            if index_tag == len(noun_index):
                break
            if 0 <= index_tag <= len(noun_index) -2:
                diff_value = noun_index[index_tag + 1] - noun_index[index_tag]
                if diff_value ==1:
                    index_tag = index_tag + 2
                    key1 = noun_index[index_tag]
                    key2 = noun_index[index_tag + 1]
                    long_key = str(words[key1])+' '+ str(words[key2])

                    final_keys.append(long_key)
                else:
                    key = noun_index[index_tag]     
                    if str(words[key]) in final_keys:
                        continue
                    final_keys.append(words[key])
            else:
                if words[index_tag] not in final_keys:
                    key = noun_index[index_tag]
                    if str(words[key]) in final_keys:
                        continue

                    final_keys.append(words[key])
                if index_tag < len(noun_index):
                    index_tag += 1

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
