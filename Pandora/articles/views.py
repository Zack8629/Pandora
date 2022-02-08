from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse

from .models import Articles


def ArticlesView(request):
    articles = Articles.objects.all()
    context = {
        "articles": articles
    }
    return render(request, template_name='articles/index.html', context=context)
