from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView

from .models import Articles, Category
from .forms import CommentCreateForm


def get_all_categories():
    return Category.objects.all()


def get_all_articles():
    return Articles.objects.all()


def articles_all(request):
    context = {
        'page_title': 'Все тексты',
        'articles': get_all_articles(),
        'categories': get_all_categories(),
    }

    return render(request, 'articles/index.html', context)


def article_view(request, slug):
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.article = get_object_or_404(Articles, slug=slug)
                if request.POST.get('parent', None):
                    new_comment.is_child = True
                    new_comment.parent_id = request.POST.get('parent')
                new_comment.save()
            return redirect('articles:article_view', slug=slug)
        else:
            return HttpResponse(status=401)
    article = get_object_or_404(Articles, slug=slug)
    comment_form = CommentCreateForm()
    context = {
        'page_title': 'Выбранная статья',
        'article': article,
        'categories': get_all_categories(),
        'comment_form': comment_form,
    }
    return render(request, 'articles/article.html', context)


class CategoryDetail(DetailView):
    model = Category
    template_name = 'articles/category_detail.html'

    def get_context_data(self, **kwargs):
        """Returns the data passed to the template"""
        selected_category = Category.objects.get(slug=self.kwargs['slug'])
        return {
            "articles": Articles.objects.filter(category__slug=self.kwargs['slug']),
            "selected_category": selected_category.title,
            'categories': get_all_categories()
        }
