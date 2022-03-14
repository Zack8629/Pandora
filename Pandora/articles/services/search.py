from articles.models import Category, Articles


def get_all_categories():
    return Category.objects.all()


def get_all_articles():
    return Articles.objects.all()