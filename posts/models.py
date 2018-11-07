from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals  import post_save
from .analyze_hindu import *

# Create your models here.


class Post(models.Model):
    text = models.TextField()
    headline = models.CharField(max_length= 500)
    pub_date = models.DateField(null=True,blank=True)
    category = models.CharField(max_length = 50)
    source = models.URLField(max_length=500)
    picture = models.URLField(max_length=500,null=True,blank=True)
    
    def __str__(self):
        return str(self.headline)

class Summary(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class Tag(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text

class TagLink(models.Model):
    title= models.CharField(max_length=100)
    tag = models.ForeignKey(Tag, on_delete= models.CASCADE)
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.tag + ' ' + self.title

class HeadlineKeyword(models.Model):
    keyword = models.CharField(max_length=50)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    entity = models.CharField(max_length=50,null=True,blank=True)
    type_nnp = models.CharField(max_length=50,null=True,blank=True)
    wiki = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.keyword

class AllCategories(models.Model):
    categories = ArrayField(models.CharField(max_length=50))

    def __str__(self):
        return str(self.categories)


#_______________________________________________________________
# post saves
def save_headline_tags(sender,instance,created,*args,**kwargs):
    if created:
        keywords = find_pos(instance.headline)
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
                headline_key.post = instance

                headline_key.save()

post_save.connect(save_headline_tags,sender=Post)
