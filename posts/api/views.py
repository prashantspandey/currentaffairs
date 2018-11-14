from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import *
from more_itertools import unique_everseen
from posts.tasks import *
import wikipedia
from dateutil.parser import parser
from django.utils.timezone import datetime 
import datetime
from datetime import timedelta

class PostHeadlineAPIView(APIView):
    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)

class ShowPostwithSummary(APIView):
    def get(self,request):
        posts = Post.objects.all()
        overall = []
        for post in posts:
            summary = post.summary_set.all()
            summa = []
            for i in summary:
                summa.append(i.text)
            summ = ''.join(summa)
            post_dict ={"id":post.id,"headline":post.headline,"body":post.text,"summary":summ,"published":post.pub_date,"category":post.category,"source":post.source}
            overall.append(post_dict)
        return Response(overall)

class PostSummary(APIView):
    def get(self,request):
        posts = Post.objects.all()
        overall = []
        for post in posts:
            summary = post.summary_set.all()
            summa = []
            for i in summary:
                summa.append(i.text)
            summ = ''.join(summa)
            post_dict ={"id":post.id,"headline":post.headline,"summary":summ,"published":post.pub_date,"category":post.category,"source":post.source}
            overall.append(post_dict)
        return Response(overall)

class PostCategorywise(APIView):
    def post(self,request,*args,**kwargs):
        category = request.POST['category']
        posts = Post.objects.filter(category=category)
        overall = []
        for post in posts:
            summary = post.summary_set.all()
            summa = []
            for i in summary:
                summa.append(i.text)
            summ = ''.join(summa)
            post_dict ={"id":post.id,"headline":post.headline,"summary":summ,"published":post.pub_date,"category":post.category,"source":post.source}
            overall.append(post_dict)
        return Response(overall)

class WholePostAPIView(APIView):
    def get(self,request):
        posts = Post.objects.all().order_by('-pub_date')[:50]
        overall = []
        for post in posts:
            headline_key_list = []
            headline_keys = post.headlinekeyword_set.all()
            for headkey in headline_keys:
                headline_key_list.append(headkey.keyword)
            summary = post.summary_set.all()
            summa = []
            for i in summary:
                summa.append(i.text)
            summ = ''.join(summa)
            

            headline_key_list = list(unique_everseen(headline_key_list))
            post_dict ={"id":post.id,"headline":post.headline,"published":post.pub_date,"summary":summa,"category":post.category,"source":post.source,'headline_keys':headline_key_list,"body":post.text,"picture":post.picture}
            overall.append(post_dict)
        return Response(overall)


class WikipediaKeywordAPIView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        keyword = data['keyword']
        word_meaning = wikipedia.summary(str(keyword))
      
        if word_meaning:
            context = {'word':keyword,'description':word_meaning}
            return Response(context)
        else:
            context = {'word':keyword,'description':'No description found.'}
            return Response(context)

class SaveCategories(APIView):
    def get(self,request):
        get_unique_categories.delay()
        return Response('saved categories')

class GetCategories(APIView):
    def get(self,request):
        all_categories = []
        categories = AllCategories.objects.all()
        for cat in categories:
            all_categories.append(cat.categories)
        category = all_categories[0]
        context = {'categories':category}
        return Response(context)

class SpecificCategoryPost(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        category =data['category']
        posts = Post.objects.filter(category=category)
        overall = []
        for post in posts:
            headline_key_list = []
            headline_keys = post.headlinekeyword_set.all()
            for headkey in headline_keys:
                headline_key_list.append(headkey.keyword)
            summary = post.summary_set.all()
            summa = []
            for i in summary:
                summa.append(i.text)
            summ = ''.join(summa)

            headline_key_list = list(unique_everseen(headline_key_list))
            post_dict ={"id":post.id,"headline":post.headline,"published":post.pub_date,"summary":summa,"category":post.category,"source":post.source,'headline_keys':headline_key_list,"body":post.text,"picture":post.picture}
            overall.append(post_dict)
        return Response(overall)

class PostByDate(APIView):
    def post(self,request,*args,**kwargs):
        data  = request.data
        date = data['date']
        dt = parse(date)
        date_final = dt.strftime('%Y-%m-%d')
        posts = Post.objects.filter(pub_date=date_final)
        overall = []
        for post in posts:
            headline_key_list = []
            headline_keys = post.headlinekeyword_set.all()
            for headkey in headline_keys:
                headline_key_list.append(headkey.keyword)
            summary = post.summary_set.all()
            summa = []
            for i in summary:
                summa.append(i.text)
            summ = ''.join(summa)

            headline_key_list = list(unique_everseen(headline_key_list))
            post_dict ={"id":post.id,"headline":post.headline,"published":post.pub_date,"summary":summa,"category":post.category,"source":post.source,'headline_keys':headline_key_list,"body":post.text,"picture":post.picture}
            overall.append(post_dict)
        return Response(overall)


class GetDates(APIView):
    def get(self,request):
        today_date = datetime.date.today()
        yesterday = today_date - timedelta(1)
        day_before = yesterday - timedelta(1)
        context = {'today':today_date,'yesterday': yesterday,'daybefore_yesterday':day_before}
        return Response(context)

class Last3DatesPosts(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        date_key = data['when']
        if date_key == 'today':
            dt = datetime.date.today()
        elif date_key == 'yesterday':
            dt = datetime.date.today() - timedelta(1)
        elif date_key == 'daybefore':
            dt = datetime.date.today() - timedelta(2)
        posts = Post.objects.filter(pub_date = dt)
        overall = []
        for post in posts:
            headline_key_list = []
            headline_keys = post.headlinekeyword_set.all()
            for headkey in headline_keys:
                headline_key_list.append(headkey.keyword)
            summary = post.summary_set.all()
            summa = []
            for i in summary:
                summa.append(i.text)
            summ = ''.join(summa)

            headline_key_list = list(unique_everseen(headline_key_list))
            post_dict ={"id":post.id,"headline":post.headline,"published":post.pub_date,"summary":summa,"category":post.category,"source":post.source,'headline_keys':headline_key_list,"body":post.text,"picture":post.picture}
            overall.append(post_dict)
        return Response(overall)

class KeywordsByType(APIView):
    def get(self,request):
        keywords = HeadlineKeyword.objects.all()
        types = []
        for keyword in keywords:
            types.append(keyword.entity)
        types = list(unique_everseen(types))
        return Response({'keyword_types':types})

class KeywordsByTypePost(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        entity = data['entity']
        if entity == "PERSON":
            keywords = HeadlineKeyword.objects.filter(entity = entity,type_nnp='PROPER')
        else:
            keywords = HeadlineKeyword.objects.filter(entity = entity)

        serializer = HeadlineKeywordSerializer(keywords,many=True)
        context = {'keywords':serializer.data}
        return Response(context)

class GetPeopleToday(APIView):
    def get(self,request):
        dt = datetime.date.today()
        people_keys = []
        keywords_posts = HeadlineKeyword.objects.filter(post__pub_date=dt)
        for key_post in keywords_posts:
            if key_post.entity =='PERSON' and key_post.type_nnp=='PROPER':
                people_keys.append(key_post.keyword)
        people_keys = list(unique_everseen(people_keys))
        context = {'people':people_keys}
        return Response(context)


class GetLocationToday(APIView):
    def get(self,request):
        dt = datetime.date.today()
        people_keys = []
        keywords_posts = HeadlineKeyword.objects.filter(post__pub_date=dt)
        for key_post in keywords_posts:
            if key_post.entity =='LOCATION':
                people_keys.append(key_post.keyword)
        people_keys = list(unique_everseen(people_keys))
        context = {'locations':people_keys}
        return Response(context)

class GetOrganizationToday(APIView):
    def get(self,request):
        dt = datetime.date.today()
        people_keys = []
        keywords_posts = HeadlineKeyword.objects.filter(post__pub_date=dt)
        for key_post in keywords_posts:
            if key_post.entity =='ORGANIZATION':
                people_keys.append(key_post.keyword)
        people_keys = list(unique_everseen(people_keys))
        context = {'organizations':people_keys}
        return Response(context)

class GetEventToday(APIView):
    def get(self,request):
        dt = datetime.date.today()
        people_keys = []
        keywords_posts = HeadlineKeyword.objects.filter(post__pub_date=dt)
        for key_post in keywords_posts:
            if key_post.entity =='EVENT':
                people_keys.append(key_post.keyword)
        people_keys = list(unique_everseen(people_keys))
        context = {'events':people_keys}
        return Response(context)
    
