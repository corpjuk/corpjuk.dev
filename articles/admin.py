from django.contrib import admin

# Register your models here.
from .models import Article

class ArticleAdmin(admin.ModelAdmin):

    #can use this to customize the display and search in admin
    list_display = ['user', 'id', 'title', 'slug', 'timestamp', 'updated']
    search_fields = ['title', 'content']
    raw_id_fields = ['user']

admin.site.register(Article, ArticleAdmin)
