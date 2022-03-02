from django.urls import path

import articles.views as articles

app_name = 'articles'

urlpatterns = [
    path('', articles.ArticlesListView.as_view(), name='index_articles'),
    path('<slug:slug>/', articles.ArticleDetailView.as_view(), name='article_view'),
    path('categories/<slug:slug>/', articles.CategoryDetail.as_view(), name='category_view'),
    path('article/create_articles/', articles.CreateArticlesView.as_view(), name='create_articles'),
    path('article/delete_article/<slug:slug>/', articles.DeleteArticlesView.as_view(), name='delete_article'),
    path('article/update_article/<slug:slug>/', articles.UpdateArticlesView.as_view(), name='update_article'),
    path('article/rating/<int:pk>/', articles.rating_add, name='rating_add'),
    path('article/comment_rating/<int:pk>/', articles.comment_rating_add, name='comment_rating_add'),
]
