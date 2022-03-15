from django import forms

from articles.models import Comment, Articles


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'published', 'content', 'category', 'summary', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
