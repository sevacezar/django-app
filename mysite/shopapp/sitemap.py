from django.contrib.sitemaps import Sitemap

from .models import Product

class ShopSitemap(Sitemap):
    changefreq = 'never'  # Как часто меняются данные на ресурсе
    priority = 0.5  # ПРиоритетт отображения в поисковиках

    def items(self):
        return Product.objects.filter(archived=False).order_by('-created_at')
    
    def lastmod(self, obj: Product):
        return obj.created_at