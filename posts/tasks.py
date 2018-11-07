from celery import shared_task
from .models import *
from .analyze_hindu import *
import datetime
from dateutil.parser import parse
from .textsummarization import *
from more_itertools import unique_everseen
import datetime
@shared_task
def testing():
    posts = Post.objects.all()
    for i in posts:
        print(i.text)


@shared_task
def add_posts_scraped(path):
    print('{} this is the past'.format(path))
    content_list = read_file(str(path)+'hindu_content.pickle')
    for num,content in enumerate(content_list):
        try:
            paras = []
            title = content['title']
            check_post = Post.objects.filter(headline = title)
            if len(check_post) > 0:
                print('already saved')
                continue

            description = content['description']
            paragraphs = content['paragraphs']
            category = content['section']
            index_date = description.index(':')
            index_final = index_date - 2
            date = description[:index_final]
            date = str(date).strip()
            dt = parse(date)
            date_final = dt.strftime('%Y-%m-%d')
            print(date_final)




            for pa in paragraphs:
                paras.append(pa)
                body = ''.join(paras)
                post = Post()
                post.text = body
                post.headline = title
                post.category = category
                print('{} category'.format(category))
                post.pub_date = date_final
                print('{} post date'.format(date_final))
                post.save()
                print('successfully saved')


        except Exception as e:
            print(str(e))
@shared_task
def live_scraping(content):
    headline = content['headline']
    date = content['date']
    story_heading = content['story_heading']
    picture = content['image']
    link = content['link']
    category = content['category']
    body = content['body']
    da_index = []
    for da_ind,da in enumerate(date):
        if da == ',':
            da_index.append(da_ind)
    

    date = date[:da_index[-1]]
    date = str(date)
    date = str(date).strip()
    dt = parse(date)
    date_final = dt.strftime('%Y-%m-%d')
    post = Post()
    post.headline = headline
    post.pub_date = date_final
    post.category = category
    post.source = link
    post.text = body
    post.picture = picture
    post.save()


    return picture
@shared_task
def delete_posts_similar():
    posts = Post.objects.all()
    print('delete the posts')
    for post in posts:
        title = post.headline
        similar_posts = Post.objects.filter(headline = title)
        if len(similar_posts) > 1:
            post.delete()
            print('Post deleted')
        else:
            print('unique post')


@shared_task
def testing_celery():
    num = 10
    for i in range(num):
        post = Post()
        post.headline = str(i) + ' testing celery'
        post.save()

@shared_task
def add_summary():
    posts = Post.objects.all()
    for post in posts:
        alreaddy_summary = post.summary_set.all()
        if len(already_symmary) > 0:
            break
        else:
            try:
                art = post.text
                summary = summarize_article(art)
                summary = ''.join(summary)
                summ = Summary()
                summ.post = post
                summ.text = summary
                summ.save()
                print('summary saved')
            except Exception as e:
                print(str(e))

@shared_task
def find_keywords_headline():
    posts = Post.objects.all()
    print('{} numb or posts kesy'.format(len(posts)))
    for num_post,post in enumerate(posts):
        old_keys = post.headlinekeyword_set.all()
        if len(old_keys) > 0:
            print('found keys')
            continue
        else:
            headline = post.headline
            print('headine {}'.format(headline))
            keywords = find_pos(headline)
            try:
                if len(keywords) != 0:
                    for key in keywords:
                        name = key['name']
                        entity = key['entity']
                        print('{} this is the key for keyword'.format(name))
                        headline_key = HeadlineKeyword()
                        wiki = key['wikipedia']
                        if wiki is not None:
                            headline_key.wiki = wiki
                        nnp = key['type_nnp']
                        if nnp is not None:
                            headline_key.type_nnp = nnp
                        headline_key.keyword = name
                        headline_key.entity = entity
                        headline_key.post = post

                        headline_key.save()
            except Exception as e:
                print(str(e))

@shared_task
def delete_keywords():
    posts = Post.objects.all()
    for post in posts:
        keys = post.headlinekeyword_set.all()
        for i in keys:
            i.delete()

@shared_task
def get_unique_categories():
    posts = Post.objects.all()
    categories = []
    for post in posts:
        category = post.category
        if category not in categories:
            categories.append(category)
    categories = list(unique_everseen(categories))
    all_categories = AllCategories()
    all_categories.categories = categories
    all_categories.save()


