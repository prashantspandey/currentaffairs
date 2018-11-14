from rest_framework import serializers
from posts.models import *

class HeadlineKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadlineKeyword
        fields = [
                'keyword',
                'entity',
                'type_nnp',
                'wiki',
                ]
class PostSerializer(serializers.ModelSerializer):
    headlinekeyword = HeadlineKeywordSerializer()
    class Meta:
        model = Post
        fields = [
            'headline',
            'text',
            'summary',
            'headlinekeyword',
            'pub_date',
            'category',
            'source'
        ]


