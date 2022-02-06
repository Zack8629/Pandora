from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import View

from articles.models import Category, Articles


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'account/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
        else:
            context = {'form': form}
            return render(request, 'account/registration.html', context)


class CreateCategoryView(CreateView):
    model = Category
    fields = ['title']
    template_name = 'account/category_create_form.html'
    success_url = reverse_lazy('account:create_category')


class CreateArticlesView(CreateView):
    model = Articles
    fields = ['title', 'content', 'category']
    template_name = 'account/articles_create_form.html'
    success_url = reverse_lazy('account:create_articles')
