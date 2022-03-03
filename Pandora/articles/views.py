from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView

from .models import Articles, Category, Comment
from .forms import CommentCreateForm
from account.models import Author


def get_all_categories():
    return Category.objects.all()


def get_all_articles():
    return Articles.objects.all()


class ContextDataMixin:
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_all_categories()
        if self.page_title is not None:
            context['page_title'] = self.page_title
        return context


class ArticlesListView(ContextDataMixin, ListView):
    model = Articles
    template_name = 'articles/index.html'
    context_object_name = "articles"
    page_title = "Все статьи"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_all_categories()
        context['articles'] = Articles.objects.filter(published=True)
        if self.page_title is not None:
            context['page_title'] = self.page_title
        return context


class ArticleDetailView(ContextDataMixin, DetailView):
    model = Articles
    context_object_name = 'article'
    template_name = 'articles/article.html'
    page_title = 'Выбранная статья'

    def post(self, *args, **kwargs):
        form = CommentCreateForm(self.request.POST)
        if self.request.user.is_authenticated:
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = self.request.user
                new_comment.article = self.get_object()
                if self.request.POST.get('parent', None):
                    new_comment.is_child = True
                    new_comment.parent_id = self.request.POST.get('parent')
                new_comment.save()
            return redirect('articles:article_view', slug=self.get_object().slug)
        else:
            return HttpResponse(status=401)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_form = CommentCreateForm()
        context['comment_form'] = comment_form
        return context


class CategoryDetail(DetailView):
    model = Category
    template_name = 'articles/index.html'

    def get_context_data(self, **kwargs):
        """Returns the data passed to the template"""
        selected_category = self.get_object()
        return {
            "articles": Articles.objects.filter(category__slug=self.kwargs['slug'], published=True),
            "selected_category": selected_category.title,
            'categories': get_all_categories()
        }


class CreateArticlesView(ContextDataMixin, SuccessMessageMixin, CreateView):
    model = Articles
    fields = ['title', 'content', 'category', 'summary', 'image']
    template_name = 'articles/articles_create_form.html'
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


class PermissionUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')
        if not request.user == self.get_object().author:
            return HttpResponseNotFound()

        return super(PermissionUserMixin, self).dispatch(request, *args, **kwargs)


class DeleteArticlesView(ContextDataMixin, PermissionUserMixin, SuccessMessageMixin, DeleteView):
    model = Articles
    template_name = 'articles/post_delete.html'
    page_title = 'Удаление статьи'
    success_message = 'Статья успешна удалена'

    def get_success_url(self):
        return reverse_lazy('account:account', kwargs={'pk': self.request.user.pk})


class UpdateArticlesView(ContextDataMixin, PermissionUserMixin, SuccessMessageMixin, UpdateView):
    model = Articles
    fields = ['title', 'published', 'content', 'category', 'summary', 'image']
    template_name = 'articles/update_article.html'
    page_title = 'Редактирование статьи'
    success_message = 'Статья успешно изменена'

    def get_success_url(self):
        return reverse_lazy('articles:article_view', kwargs={'slug': self.get_object().slug})


def like_dislike_rating(obj, user,likes, dislikes):
    if dislikes == 'true':
        obj.like.remove(user)
        obj.dislike.add(user)
    else:
        obj.dislike.remove(user)

    if likes == 'true':
        obj.dislike.remove(user)
        obj.like.add(user)
    else:
        obj.like.remove(user)


def rating_add(request, pk=None):
    if request.method == 'POST':
        likes = request.POST.get('like')
        dislikes = request.POST.get('dislike')
        user = Author.objects.get(username=request.user.username)
        article = Articles.objects.get(pk=pk)

        like_dislike_rating(article, user, likes, dislikes)

    return JsonResponse({})


def comment_rating_add(request, pk=None):
    if request.method == 'POST':
        likes = request.POST.get('like')
        dislikes = request.POST.get('dislike')
        user = Author.objects.get(username=request.user.username)
        comment = Comment.objects.get(pk=pk)

        like_dislike_rating(comment, user, likes, dislikes)

    return JsonResponse({})