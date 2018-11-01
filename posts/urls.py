from django.urls import path
from .views import *


app_name = 'posts'

urlpatterns = [

    path('home/',home,name="Posts"),
    path('scraped/',scrape,name="Scrape"),
    path('delete_posts/',delete_posts,name="DeletePosts"),
    path('test_celery/',test_celery,name="testcelery"),
    path('add_summary/',add_summary_view,name="Summary"),
    path('add_keywords_headline/',find_keywords,name="HeadlineKeywords"),
]
