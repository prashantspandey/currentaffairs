from celery import shared_task
from .models import *
from .analyze_hindu import *
import datetime
from dateutil.parser import parse
from .textsummarization import *

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
def delete_posts_similar():
    posts = Post.objects.all()
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


