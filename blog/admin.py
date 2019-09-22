from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date','author')
    search_fields = ('title','text')
admin.site.register(Post, PostAdmin)