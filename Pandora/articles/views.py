from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from .models import Articles, Category


def get_all_categories():
    return Category.objects.all()


def get_all_articles():
    return Articles.objects.all()


def articles_all(request):
    context = {
        'page_title': 'Все тексты',
        'articles': get_all_articles(),
        'categories': get_all_categories(),
    }

    return render(request, 'articles/index.html', context)


def article_view(request, pk):
    article = get_object_or_404(Articles, pk=pk)
    context = {
        'page_title': 'Выбранная статья',
        'article': article,
        'categories': get_all_categories(),
    }

    return render(request, 'articles/article.html', context)


# def category_view(request, pk):
#     context = {
#         'page_title': 'Выбранный раздел',
#         'articles': get_all_articles(),
#         'categories': get_all_categories(),
#     }
#
#     return render(request, 'articles/index.html', context)


class CategoryDetail(DetailView):
    model = Category
    template_name = 'articles/category_detail.html'
    context_object_name = 'category'

    def get_object(self, queryset=None):
        return Category.objects.get(id=self.kwargs['pk'])
