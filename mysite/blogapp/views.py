from django.contrib.syndication.views import Feed
from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy


from .models import Article, ArticleDemo

# Create your views here.
class ArticleListView(ListView):
    queryset = (Article.objects
                .select_related('author')
                .select_related('category')
                .prefetch_related('tags')
                .defer('content'))
    

class ArticlesDemoList(ListView):
    queryset = ArticleDemo.objects.filter(published_at__isnull=False).order_by("-published_at")

class ArticleDemoDetailView(DetailView):
    model = ArticleDemo


class LatestArticlesFeed(Feed):
    title = 'Blog articles (latest)'  # Заголовок ленты
    description = 'Updates on changes and addition blog articles'  # Подробное описание
    link = reverse_lazy('blogapp:articles')  #  Ссылка на домашню страницу

    def items(self):
        """Информация о статьях в списке ленты.
        Явное ограничение количества отоборажения (5)"""
        return ArticleDemo.objects.filter(published_at__isnull=False).order_by("-published_at")[:5]
    
    def item_title(self, item: ArticleDemo):
        """Получение заголовка из списка объектов"""
        return item.title
    
    def item_description(self, item: ArticleDemo) -> str:
        """Получение короткой информации о статье (для ознакомления, срезом)"""
        return item.body[:200]
    
    def item_link(self, item: ArticleDemo):
        """Перенаправление на всю статью целиком"""
        return reverse('blogapp:article', kwargs={'pk': item.pk})

    