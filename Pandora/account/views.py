from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import DetailView, UpdateView, ListView, CreateView

from django.views.generic.base import View

from articles.models import Articles, ErrorMessageModeration
from articles.views import ContextDataMixin
from .forms import CustomUserCreateForm, AuthorForm, ErrorMessageModerationForm
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


class AccountPersonalData(ContextDataMixin, DetailView):
    model = Author
    template_name = "account/account_personal_data.html"
    page_title = 'Личные данные'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['articles'] = Articles.objects.filter(author=pk)

        return context


class AdminAccountView(ContextDataMixin, DetailView):
    model = Author
    template_name = "account/admin_account.html"
    page_title = 'Личный кабинет админа'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(AdminAccountView, self).dispatch(request, *args, **kwargs)
        return HttpResponseNotFound()


class ModeratorAccountView(ContextDataMixin, DetailView):
    model = Author
    template_name = "account/moderator_account.html"
    page_title = 'Личный кабинет модератора'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_template = self.kwargs.get('type')
        context['type_context'] = type_template
        if type_template == 'moder_article':
            context['articles_view'] = Articles.moderation_article()
        if type_template == 'moder_user':
            context['users'] = Author.objects.all()

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_moderator:
            return super(ModeratorAccountView, self).dispatch(request, *args, **kwargs)
        return HttpResponseNotFound()


class NotApproveMessage(CreateView):
    form_class = ErrorMessageModerationForm
    model = ErrorMessageModeration
    template_name = 'account/moderation_message_form.html'

    def get_success_url(self):
        return reverse_lazy('account:moder_account', kwargs={'type': 'moder_article','pk': self.kwargs.get('id_moder')})

    def form_valid(self, form, *args, **kwargs):
        form.save(commit=False)
        author = self.request.user
        form.instance.author = author
        article_id = self.kwargs.get('article_id')
        message = form.save()
        object_article = Articles.objects.filter(pk=article_id).first()
        object_article.for_moderation = Articles.ERROR_MODERATION
        object_article.message_moderation.add(message)
        object_article.save()
        return super(NotApproveMessage, self).form_valid(form)


def approve_moder_article(request, type=None, pk=None):
    if request.method == 'GET':
        if request.user.is_moderator:
            if pk is not None:
                article = Articles.objects.filter(pk=pk).first()
                if article:
                    if type == 'approve':
                        article.for_moderation = Articles.NOT_MODERATION
                        article.published = True
                        for message in article.message_moderation.all():
                            message.is_active = False

                    article.save()
        return JsonResponse({})

def block_user_view(request, pk=None):
    if request.method == 'GET':
        if request.user.is_superuser or request.user.is_moderator:
            if pk is not None:
                author = Author.objects.filter(pk=pk).first()
                if author:
                    if not author.is_superuser or not request.user.is_moderator:
                        if author.is_active:
                            author.is_active = False
                        else:
                            author.is_active = True
                        author.save()
        return JsonResponse({})

def give_rights_moderator(request, pk=None):
    if request.method == 'GET':
        if request.user.is_superuser:
            if pk is not None:
                author = Author.objects.filter(pk=pk).first()
                if author:
                    if not author.is_superuser:
                        if author.is_moderator:
                            author.is_moderator = False
                        else:
                            author.is_moderator = True
                        author.save()
        return JsonResponse({})


class AccountArticles(ContextDataMixin, DetailView):
    model = Author
    template_name = "account/account_articles.html"
    page_title = 'Личный кабинет - статьи'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        type_article = self.kwargs.get('type')
        context = super().get_context_data(**kwargs)
        if type_article == 'published':
            context['articles'] = Articles.author_published_article(pk)
            context['type'] = 'published'

        if type_article == 'draft':
            context['articles'] = Articles.author_draft_article(pk)
            context['type'] = 'draft'

        if type_article == 'moderation':
            context['articles'] = Articles.author_moderation_article(pk)
            context['type'] = 'moderation'

        if type_article == 'error_moderation':
            context['articles'] = Articles.author_error_moderation_article(pk)
            context['type'] = 'error_moderation'

        return context

    def dispatch(self, request, *args, **kwargs):
        type_article = self.kwargs.get('type')
        if not self.request.user.is_authenticated or self.request.user.pk != kwargs.get('pk'):
            if type_article == 'draft':
                return HttpResponseNotFound()
            if type_article == 'moderation':
                return HttpResponseNotFound()
            if type_article == 'error_moderation':
                return HttpResponseNotFound()

        return super(AccountArticles, self).dispatch(request, *args, **kwargs)


class AccountUpdateView(ContextDataMixin, ProperUserMixin, SuccessMessageMixin, UpdateView):
    form_class = AuthorForm
    model = Author
    template_name = 'account/update_account.html'
    page_title = 'Изменение профайла'
    success_message = 'Данные успешно изменены'

    def get_success_url(self):
        return reverse_lazy('account:personal_data', kwargs={'pk': self.request.user.pk})


def rating_change(request, pk=None):
    print("rating changed", pk)
    return render('account/moderator_account.html')
