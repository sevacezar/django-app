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
        self.stdout.write('Creating order...')
        user = User.objects.first()
        products = Product.objects.only('id').all()

        order, created = Order.objects.get_or_create(
            delivary_address='NEWWWWWssssssss',
            promocode='PROMOsss',
            user=user,
        )
        # order + 1  # error to fix transaction
        for product in products:
            order.products.add(product)
        
        order.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Created order {order}'
            )
        )