from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

import account.views as account

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(next_page='/'), name='login'),
    path('update/<int:pk>/', account.AccountUpdateView.as_view(), name='update'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', account.RegistrationView.as_view(), name='registration'),
    path('<int:pk>/', account.AccountDetailView.as_view(), name='account'),
]
