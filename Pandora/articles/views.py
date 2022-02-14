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


def article_view(request, slug):
    article = get_object_or_404(Articles, slug=slug)
    context = {
        'page_title': 'Выбранная статья',
        'article': article,
        'categories': get_all_categories(),
    }

    return render(request, 'articles/article.html', context)


class CategoryDetail(DetailView):
    model = Category
    template_name = 'articles/category_detail.html'
    selected_category = get_all_categories().filter(id=1)

    def get_context_data(self, **kwargs):
        """Returns the data passed to the template"""
        selected_category = Category.objects.get(slug=self.kwargs['slug'])
        return {
            "articles": Articles.objects.filter(category__slug=self.kwargs['slug']),
            "selected_category": selected_category.title,
            'categories': get_all_categories()
        }
