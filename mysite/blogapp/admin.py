from django.contrib import admin

from .models import ArticleDemo


@admin.register(ArticleDemo)
class ArticleDemoAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'body', 'published_at'
