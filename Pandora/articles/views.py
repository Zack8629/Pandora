from django.shortcuts import render, get_object_or_404

from .models import Articles, Category


def get_all_categories():
    return Category.objects.all()


def articles_all(request):
    articles = Articles.objects.all()
    context = {
        'page_title': 'Все тексты',
        'articles': articles,
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

    return render(request, 'articles/article_view.html', context)


def category_view(request, pk):
    articles = Articles.objects.all()
    context = {
        'page_title': 'Выбранный раздел',
        'articles': articles,
        'categories': get_all_categories(),
    }
<<<<<<< HEAD
    return render(request, template_name='articles/index.html', context=context)
=======

    return render(request, 'articles/category_view.html', context)
>>>>>>> controllers
