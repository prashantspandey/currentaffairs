from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class Post(models.Model):
    text = models.TextField()
    headline = models.CharField(max_length= 500)
    pub_date = models.DateField(null=True,blank=True)
    category = models.CharField(max_length = 50)
    source = models.URLField(max_length=500)
    
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
