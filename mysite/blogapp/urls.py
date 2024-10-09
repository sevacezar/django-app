from django.urls import path, include

from .views import ArticleListView, ArticleDemoDetailView, ArticlesDemoList, LatestArticlesFeed

app_name = 'blogapp'

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles_list'),
    path('articles_demo/', ArticlesDemoList.as_view(), name='articles'),
    path('articles_demo/<int:pk>/', ArticleDemoDetailView.as_view(), name='article'),
    path('articles_demo/latest/feed/', LatestArticlesFeed(), name='articles-feed'),
]