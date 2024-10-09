from django.core.management import BaseCommand

from blogapp.models import Tag

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start tags creation')
        tags = [
            'moto',
            'drive',
            'cars',
            'food',
            'vegeterianism',
        ]
        tags_objs = [
            Tag(name=tag)
            for tag in tags
        ]
        Tag.objects.bulk_create(tags_objs)
        self.stdout.write('Creation is done')
