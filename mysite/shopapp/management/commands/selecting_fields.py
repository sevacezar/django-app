from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Product

class Command(BaseCommand):
    """
    Creates order
    """
    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')
        users_info = User.objects.values_list('pk', 'username')
        for u in users_info:
            print(u)

        # product_values = Product.objects.values('pk', 'name')
        # for p_values in product_values:
        #     print(p_values)
        self.stdout.write('DONE')