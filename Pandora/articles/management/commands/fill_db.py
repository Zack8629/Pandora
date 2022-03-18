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
        categories = load_from_json('articles/json/category.json')
        articles = load_from_json('articles/json/articles.json')
        num_users = 5
        category_id = []
        authors_id = []

        if not Author.objects.filter(username='admin').exists():
            Author.objects.create_superuser('admin', 'admin@mail.local', 'admin')

        for i in range(num_users):
            _user = f'user_{i + 1}'
            if not Author.objects.filter(username=f'{_user}').exists():
                Author.objects.create_user(username=f'{_user}',
                                           first_name=f'{_user}',
                                           last_name=f'{_user}',
                                           email=f'{_user}@mail.local',
                                           password='geekbrains')
            authors_id.append(Author.objects.get(username=f'{_user}').id)
        print('all users created!')

        for category in categories:
            if not Category.objects.filter(title=f'{category["title"]}').exists():
                Category.objects.create(**category)
            category_id.append(Category.objects.get(title=f'{category["title"]}').id)
        print('all category created!')

        def get_category_id(_category_id):
            while True:
                for _id in _category_id:
                    yield _id

        def get_author_id(_authors_id):
            while True:
                for _id in _authors_id:
                    yield _id

        _category_id = get_category_id(category_id)
        _author_id = get_author_id(authors_id)
        for article in articles:
            if not Articles.objects.filter(title=f'{article["title"]}').exists():
                Articles.objects.create(category_id=next(_category_id),
                                        author_id=next(_author_id),
                                        **article)
        print('all articles created!')

        print('All done!')
