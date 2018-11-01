from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Post)
admin.site.register(Summary)
admin.site.register(Tag)
admin.site.register(TagLink)
admin.site.register(HeadlineKeyword)

