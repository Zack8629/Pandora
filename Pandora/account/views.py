from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView
from django.views.generic.base import View

from articles.models import Category, Articles
from articles.views import get_all_articles, get_all_categories

from .forms import CustomUserCreateForm
from .models import Author


class RegistrationView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = CustomUserCreateForm()
        context = {'form': form}
        return render(request, 'account/registration.html', context)

    @staticmethod
    def post(request, *args, **kwargs):
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
        else:
            context = {'form': form}
            return render(request, 'account/registration.html', context)


class ProperUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('articles:index_articles')
        if not request.user.pk == kwargs.get('pk'):
            return HttpResponseNotFound()
        return super(ProperUserMixin, self).dispatch(request, *args, **kwargs)


class AccountDetailView(ProperUserMixin, DetailView):
    model = Author
    template_name = "account/account.html"
    # pk = self.kwargs['pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Личный кабинет'
        # context['articles'] = Articles.objects.filter(author=pk)
        context['categories'] = get_all_categories()
        # pk = self.kwargs['pk']
        # print(pk)
        return context


class CreateCategoryView(ProperUserMixin, CreateView):
    model = Category
    fields = ['title']
    template_name = 'account/category_create_form.html'
    success_url = reverse_lazy('account:create_category')


class CreateArticlesView(ProperUserMixin, CreateView):
    model = Articles
    fields = ['title', 'content', 'category']
    template_name = 'account/articles_create_form.html'
    success_url = reverse_lazy('account:create_articles')
