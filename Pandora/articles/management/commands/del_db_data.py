from django.core.management.base import BaseCommand

from account.models import Author
from articles.models import Category, Articles


class Command(BaseCommand):
    def handle(self, *args, **options):
        Articles.objects.all().delete()
        Category.objects.all().delete()
        Author.objects.all().delete()
        print('All data has been deleted!')
