from django.db.models import Q

from articles.models import Category, Articles


def get_all_categories():
    return Category.objects.all()


def get_all_articles():
    return Articles.objects.all()


def sorting_articles(**kwargs):
    sorting = kwargs.get('sorting')
    field = kwargs.get('field')
    if sorting and field:
        sorting = sorting[0]
        field = field[0]
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


def search_article(value, query):

    if value is not None:


        query = query.filter(
            Q(title__icontains=value) |
            Q(summary__icontains=value) |
            Q(author__username__icontains=value)|
            Q(category__title__icontains=value)

        )

        return query
    else:
        return query