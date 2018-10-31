from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import re
import pickle
from more_itertools import unique_everseen
from collections import Counter
import numpy as np
import random


def summa(text, lexicon):
    scores = []
    text = [i.lower() for i in text]
    sent_word = [word_tokenize(i) for i in text]
    tok = np.zeros(len(lexicon))
    for k in range(len(sent_word)):
        for i in sent_word[k]:

            if i in lexicon:
                index_value = lexicon.index(i)
                tok[index_value] += 1
            else:
                index_value = 0
        features = list(tok)
        tok[index_value] = 0

        fet = np.array(features)
        sum = np.sum(features)
        scores.append(sum)

   # print(scores)
   # print(np.argmax(scores))
    ind = np.argmax(scores)

    u = []
    v = []

    for i, n in enumerate(scores):
        u.append(int(i))
        v.append(int(n))
    inde = list(zip(u, v))

    inde = np.array(inde)
    kkk = np.sort(inde[:, 1])
    las = []
    ret = []
    for i in reversed(kkk):
        las.append(np.where(inde[:, 1] == i))
    for j in range(5):
        try:
            l = las[j][0].flatten()
            ret.append(l)
        except Exception as e:
            pass
            for tr in range(1):
                ret.append(las[tr][0])
    return ret


def pre_processing(art, mi, ma):
    q1 = '–'
    q2 = 'Related'
    q3= 'Image'
    q4 = ':'
    q5 = 'Video'
    q6 = r'\\xa0'
    qw = list(q1)+list(q2)+list(q3)+list(q4)+ list(q5) + list(q6)
    stop = set(stopwords.words('english') + list(punctuation) + qw)
    token_list = []

    art = ''.join(art)
    art2 = ''.join(art)

    art = [i for i in art.split()]
    art2 = [i for i in art2.split('.')]

    for i in art:
        if i.lower() not in stop:
            token_list.append(i.lower())
    min_percent = int(int(len(token_list) / 100) * mi)
    max_percent = int(int(len(token_list) / 100) * ma)
    w_count = Counter(token_list)
    l2 = []
    for w in w_count:
        if max_percent > w_count[w] > min_percent:
            l2.append(w)
    l2 = list(unique_everseen(l2))
    if len(l2) == 0 or 1:
        min_percent = int(int(len(token_list) / 100) * 1)
        max_percent = int(int(len(token_list) / 100) * 99)
        for w in w_count:
            if max_percent > w_count[w] > min_percent:
                l2.append(w)
        l2 = list(unique_everseen(l2))
        if len(l2) == 0:
            for w in w_count:
                l2.append(w)
            l2 = list(unique_everseen(l2))
        else:
            pass
    else:
        pass

    return l2, art2


def summarize_article(art):
    help_list = []
    lexicon,article = pre_processing(art,10,95)
    ind_list = summa(article,lexicon)
    ind_list = np.array(ind_list)
    ind_list = ind_list.flatten()
    try:
        ind_list.sort()
        for i in ind_list:
            help_list.append(article[i])
        help_list = list(unique_everseen(help_list))
    except Exception as e:
        pass
    final_list = []
    try:
        for i in ind_list:
            for j in i:
                final_list.append(j)
        final_list = list(unique_everseen(final_list))
        final_list.sort()
        for wq in final_list: 
            help_list.append(article[wq])
        help_list = list(unique_everseen(help_list))
    except Exception as e:
        pass
    return help_list

'''
        pp = []
        rea = []
        rav = []
        all_articles = []
        new_li = []
        for k,y in enumerate(li):
            help_list = []
            print('Summarizing article number %d' % k)
            if k==115 or k==402 or k==406 or k==407 or k==408 or k==409 or k==419 or k==3029:
                continue
            lexicon, article = pre_processing(y, 10, 95)
            print('Length of lexicon %d' % (int(len(lexicon))))
            print('%d sentences in the article ' % (int(len(article))))
            print(lexicon)
            ind_list = summa(article, lexicon)
            ind_list = np.array(ind_list)
            print(ind_list.shape)
            print('List before flattening %s' % (str(ind_list)))
            ind_list = ind_list.flatten()
            print('List is of shape %d  after flattening ' % ind_list.shape)
            # ind_list = list(unique_everseen(ind_list))
            # ind_list.sort()
            print('%d is the length of index list after flatenning' % (len(ind_list)))
            try:
                ind_list.sort()
                for wq in ind_list:
                    help_list.append(article[wq])
                help_list = list(unique_everseen(help_list))
                all_articles.append(help_list)
            except Exception as e:
                print(str(e))
            print('index list: %s' % (ind_list))
            final_list = []

            try:

                for i in ind_list:
                    for j in i:
                        final_list.append(j)
                final_list = list(unique_everseen(final_list))
                final_list.sort()
                print('Final list: %s' % (final_list))
                for wq in final_list:
                    help_list.append(article[wq])
                help_list = list(unique_everseen(help_list))
                all_articles.append(help_list)
                # with open('summarizedtextlong.txt', 'a', encoding='utf-8') as final_write:
                #     for line in final_list:
                #         final_write.write(article[line])
                #         if line == final_list[-1]:
                #             final_write.write(article[line] + '\n\n')

            except Exception as e:
                print(str(e))
                # with open('summarizedtextlong.txt', 'a', encoding='utf-8') as final_write:
                #     for line in ind_list:
                #         final_write.write(article[line])
                #         if line == ind_list[-1]:
                #             final_write.write(article[line] + '\n\n')
        print(len(all_articles))
        all_articles = list(unique_everseen(all_articles))
        print(len(all_articles))
        print('successfully written to text file')
        with open('allarticlessummarized10-95.pkl','wb') as allar:
            pickle.dump(all_articles,allar)
        print('successfully dumped the pickle file')
'''
