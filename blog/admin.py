from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date','author')
    search_fields = ('title','text')
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','name','created','active')
    list_filter = ('post','active')
    search_fields = ('text','name')
admin.site.register(Comment, CommentAdmin)