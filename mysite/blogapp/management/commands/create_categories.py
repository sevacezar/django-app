from django.core.management import BaseCommand

from blogapp.models import Category

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Start categories creation')
        categories = [
            'scince',
            'it',
            'health',
            'sport',
            'entertainments',
        ]
        categories_objs = [
            Category(name=category)
            for category in categories
        ]
        Category.objects.bulk_create(categories_objs)
        self.stdout.write('Creation is done')
