from django.shortcuts import render
from django.http import HttpResponse
from .tasks import *
from .models import *

# Create your views here.


def home(request):
    user = request.user
    if user.is_staff:
        testing.delay()

    return HttpResponse('hello')

def scrape(request):
    user = request.user
    if user.is_staff:
        add_posts_scraped('/home/prashantbodhi/currentaffairs/currentaffairs/posts/pickles/')

    return HttpResponse('scraped')

def delete_posts(request):
    print('here in delete')
    delete_posts_similar.delay()
    return HttpResponse('deleted')

def test_celery(request):
    testing_celery.delay()
    return HttpResponse('tested')

def add_summary_view(request):
    add_summary.delay()
    print('summary added')
    return HttpResponse('summary')

def find_keywords(request):
    find_keywords_headline.delay()
    return HttpResponse('saved')

def delete_headline_keywords(request):
    delete_keywords.delay()
    return HttpResponse('delted')
