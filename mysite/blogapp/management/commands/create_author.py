from django.core.management import BaseCommand

from blogapp.models import Author

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start authors creation')
        authors = [
            {'name': 'Tom', 'bio': 'Bio of Tom'},
            {'name': 'Alex', 'bio': 'Bio of Alex'},
            {'name': 'Daniel', 'bio': 'Bio of Daniel'}
        ]
        authors_objs = [
            Author(name=author['name'], bio=author['bio'])
            for author in authors
        ]
        Author.objects.bulk_create(authors_objs)
        self.stdout.write('Creation is done')
