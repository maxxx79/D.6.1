from django.contrib import admin

# Register your models here.
from .models import Category, Author, Comment, Post, PostCategory, UserCategory

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(UserCategory)
