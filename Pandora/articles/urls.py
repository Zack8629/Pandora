from django.urls import path

from .views import Articles

urlpatterns = [
    path('', Articles),
]