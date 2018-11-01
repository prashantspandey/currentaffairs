from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import *
from more_itertools import unique_everseen


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
        posts = Post.objects.all()[:50]
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
            post_dict ={"id":post.id,"headline":post.headline,"published":post.pub_date,"summary":summa,"category":post.category,"source":post.source,'headline_keys':headline_key_list,"body":post.text}
            overall.append(post_dict)
        return Response(overall)



