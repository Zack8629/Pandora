from django.urls import path

import articles.views as articles

app_name = 'articles'

urlpatterns = [
    path('', articles.articles_all, name='index_articles'),
    path('<slug:slug>/', articles.article_view, name='article_view'),
    path('categories/<slug:slug>/', articles.CategoryDetail.as_view(), name='category_view'),
]
