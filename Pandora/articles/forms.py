from django import forms
from articles.models import Comment


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']


