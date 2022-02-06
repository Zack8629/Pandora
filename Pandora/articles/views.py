from django.shortcuts import render
from .models import Articles


def ArticlesView(request):
    articles = Articles.objects.all()
    context = {
        "articles": articles
    }
    return render(request, template_name='articles/index.html', context=context)
