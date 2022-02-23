from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import View

from articles.models import Articles
from articles.views import ContextDataMixin, PermissionUserMixin

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


class AccountDetailView(ContextDataMixin, ProperUserMixin, DetailView):
    model = Author
    template_name = "account/account.html"
    page_title = 'Личный кабинет'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['articles'] = Articles.objects.filter(author=pk)

        return context


class AccountUpdateView(ContextDataMixin, ProperUserMixin, SuccessMessageMixin, UpdateView):
    model = Author
    fields = ['username', 'first_name', 'last_name', 'email', 'about_me', 'birthday']
    template_name = 'account/update_account.html'
    page_title = 'Изменение профайла'
    success_message = 'Данные успешно изменены'

    def get_success_url(self):
        return reverse_lazy('account:account', kwargs={'pk': self.request.user.pk})
