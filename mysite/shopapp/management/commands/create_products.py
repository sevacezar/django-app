from django.core.management import BaseCommand

from shopapp.models import Product

class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):
        self.stdout.write('Creating products...')

        products = [
            {'name': 'Iphone', 'description': 'Best mobile phone', 'price': 1000},
            {'name': 'MacAir', 'description': 'Best laptop', 'price': 1300},
            {'name': 'AirPods', 'description': 'Best earphones', 'price': 250},
        ]

        for product in products:
            product, created = Product.objects.get_or_create(**product)
            self.stdout.write(f'Created product {product.name}')
        self.stdout.write(self.style.SUCCESS('Products created!'))