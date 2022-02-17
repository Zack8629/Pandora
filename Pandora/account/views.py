from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.views.generic.base import View, TemplateView

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


class ProperUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('articles:index_articles')
        if not request.user.pk == kwargs.get('pk'):
            return HttpResponseNotFound()
        return super(ProperUserMixin, self).dispatch(request, *args, **kwargs)


class ContextDataMixin:
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_all_categories()
        if self.page_title is not None:
            context['page_title'] = self.page_title
        return context


class AccountDetailView(ContextDataMixin, ProperUserMixin, DetailView):
    model = Author
    template_name = "account/account.html"
    page_title = 'Личный кабинет'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['articles'] = Articles.objects.filter(author=pk)

        return context


class CreateCategoryView(CreateView):
    model = Category
    fields = ['title']
    template_name = 'account/category_create_form.html'
    success_url = reverse_lazy('account:create_category')


class CreateArticlesView(ContextDataMixin, SuccessMessageMixin, CreateView):
    model = Articles
    fields = ['title', 'content', 'category']
    template_name = 'account/articles_create_form.html'
    page_title = 'Создание статьи'
    success_message = 'Статья успешна создана'

    def get_success_url(self):
        return reverse_lazy('account:account', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form, *args, **kwargs):
        form.save(commit=False)
        author = self.request.user
        form.instance.author = author
        form.save()
        return super(CreateArticlesView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        return super(CreateArticlesView, self).dispatch(request, *args, **kwargs)


class DeleteArticlesView(ContextDataMixin, SuccessMessageMixin, DeleteView):
    model = Articles
    template_name = 'account/post_delete.html'
    page_title = 'Удаление статьи'
    success_message = 'Статья успешна удалена'

    def get_success_url(self):
        return reverse_lazy('account:account', kwargs={'pk': self.request.user.pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        if not request.user == self.get_object().author:
            return HttpResponseNotFound()

        return super(DeleteArticlesView, self).dispatch(request, *args, **kwargs)


class UpdateArticlesView(ContextDataMixin, SuccessMessageMixin, UpdateView):
    model = Articles
    fields = ['title', 'content', 'category']
    template_name = 'account/update_article.html'
    page_title = 'Редактирование статьи'
    success_message = 'Статья успешна изменена'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        if not request.user == self.get_object().author:
            return HttpResponseNotFound()

        return super(UpdateArticlesView, self).dispatch(request, *args, **kwargs)
