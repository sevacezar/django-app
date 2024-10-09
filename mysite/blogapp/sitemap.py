from django.contrib.sitemaps import Sitemap

from .models import ArticleDemo

class BlogSitemap(Sitemap):
    changefreq = 'never'  # Как часто меняются данные на ресурсе
    priority = 0.5  # ПРиоритетт отображения в поисковиках

    def items(self):
        return ArticleDemo.objects.filter(published_at__isnull=False).order_by('-published_at')
    
    def lastmod(self, obj: ArticleDemo):
        return obj.published_at