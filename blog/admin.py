from atexit import register
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Post

# Register your models here.

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Post)
