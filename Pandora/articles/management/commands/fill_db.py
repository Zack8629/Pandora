import json

from django.core.management.base import BaseCommand

from account.models import Author
from articles.models import Category, Articles


def load_from_json(file_name):
    with open(file_name, encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill data in db'

    def handle(self, *args, **options):
        if not Author.objects.filter(username='admin').exists():
            Author.objects.create_superuser('admin', 'admin@no.local', 'admin')

        num_users = 5
        for i in range(num_users):
            _user = f'user_{i+1}'
            if not Author.objects.filter(username=f'{_user}').exists():
                Author.objects.create_user(username=f'{_user}',
                                           first_name=f'{_user}',
                                           last_name=f'{_user}',
                                           email=f'{_user}@mail.local',
                                           password='password')
        print('all users created!')

        items = load_from_json('articles/json/category.json')
        for item in items:
            if not Category.objects.filter(title=f'{item["title"]}').exists():
                Category.objects.create(**item)
        print('all category created!')

        items = load_from_json('articles/json/articles.json')
        for item in items:
            if not Articles.objects.filter(title=f'{item["title"]}').exists():
                Articles.objects.create(**item)
        print('all articles created!')

        print('All done!')
