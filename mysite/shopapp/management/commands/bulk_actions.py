from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from shopapp.models import Product, Order

class Command(BaseCommand):
    """
    Creates order
    """
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Start demo bulk actions')
        res = Product.objects.filter(
            name__contains='iphone',
        ).update(discount=10)

        print(res)
        # info = [
        #     ('iphone 1', 200),
        #     ('iphone 2', 200),
        #     ('iphone 3', 200),
        #     ('iphone 4', 200),

        # ]

        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]

        # res = Product.objects.bulk_create(products)
        # for obj in res:
        #     print(obj)

        self.stdout.write('DONE')