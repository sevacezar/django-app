from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Author, Category, Article, Tag

class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Start articles creation')
        authors = Author.objects.all()
        tags = Tag.objects.all()
        categories = Category.objects.all()

        contents = [
            f'Content of article #{i}' + 'Content\t' * 1000
            for i in range(1, 3)
        ]
        titles = ['Motos and cars sport', 'Healthy food']

        article1 = Article(
            title = titles[0],
            content = contents[0],
            author = authors[0],
            category = categories[3],
        )

        article2 = Article(
            title = titles[1],
            content = contents[1],
            author = authors[1],
            category = categories[2],
        )

        articles = Article.objects.bulk_create([article1, article2])
        articles[0].tags.add(tags[0], tags[1], tags[2])
        articles[1].tags.add(tags[3], tags[4])

        self.stdout.write('Creation is done')
