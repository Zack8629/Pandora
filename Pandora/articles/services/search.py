from articles.models import Category, Articles


def get_all_categories():
    return Category.objects.all()


def get_all_articles():
    return Articles.objects.all()


def sorting_articles(**kwargs):
    sorting = kwargs.get('sorting')[0]
    field = kwargs.get('field')[0]
    ordering_field = 'created_at'
    if sorting == 'asc':
        sorting_field = ''
    else:
        sorting_field = '-'

    if field == 'data':
        ordering_field = 'created_at'

    if field == 'rating':
        ordering_field = 'views'

    if field == 'comment':
        ordering_field = 'quantity_comment'

    if field == 'like':
        ordering_field = 'like'

    return sorting_field + ordering_field


