from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import RegistrationView, CreateCategoryView, CreateArticlesView


app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(next_page='/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('create_category/', CreateCategoryView.as_view(), name='create_category'),
    path('create_articles/', CreateArticlesView.as_view(), name='create_articles')


]
