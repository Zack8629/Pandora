from django.urls import path

<<<<<<< HEAD
from .views import ArticlesView

urlpatterns = [
    path('', ArticlesView)
]
=======
import articles.views as articles

app_name = 'articles'

urlpatterns = [
    path('', articles.articles_all, name='index_articles'),
    path('article_<int:pk>/', articles.article_view, name='article_view'),
    path('hub_<int:pk>/', articles.category_view, name='category_view'),
]
>>>>>>> controllers
