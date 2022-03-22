from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

import account.views as account

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(next_page='/'), name='login'),
    path('update/<int:pk>/', account.AccountUpdateView.as_view(), name='update'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', account.RegistrationView.as_view(), name='registration'),
    path('<int:pk>/', account.AccountPersonalData.as_view(), name='personal_data'),
    path('<int:pk>/my_articles/<str:type>/', account.AccountArticles.as_view(), name='my_articles'),
]
