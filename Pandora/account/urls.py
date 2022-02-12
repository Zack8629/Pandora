from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

import account.views as account

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(next_page='/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', account.RegistrationView.as_view(), name='registration'),
    path('create_category/', account.CreateCategoryView.as_view(), name='create_category'),
    path('create_articles/', account.CreateArticlesView.as_view(), name='create_articles'),
    path('<int:pk>/', account.AccountDetailView.as_view(), name='account')
]
