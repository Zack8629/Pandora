from django.urls import path

from .views import ArticlesView

urlpatterns = [
    path('', ArticlesView)
]