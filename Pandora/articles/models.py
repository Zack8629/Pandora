from django.db.models import F
from django.utils.text import slugify

from .utils import alphabet
from time import time

from django.db import models
from account.models import Author


def gen_slug(title, model_type=None):
    if model_type:
        eng_title = ''.join(alphabet.get(c, c) for c in title.lower())
        slug_field = ' '.join(eng_title.split()[:4]) + '-' + str(time())[-5:]
    else:
        slug_field = ''.join(alphabet.get(c, c) for c in title.lower())
    return slugify(slug_field, allow_unicode=True)


class Category(models.Model):
    """Defining articles categories"""
    title = models.CharField(max_length=150, db_index=True, verbose_name="Заголовки категорий")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]


class Rating:

    def get_list_user_likes(self):
        list_username = [user.username for user in self.like.all()]
        return list_username

    def get_list_user_dislikes(self):
        list_username = [user.username for user in self.dislike.all()]
        return list_username

    def get_likes(self):
        likes = len(self.like.all())
        return likes

    def get_dislikes(self):
        dislikes = len(self.dislike.all())
        return dislikes

class Articles(models.Model, Rating):
    """We create articles with the necessary fields and categories"""
    title = models.CharField(max_length=150, db_index=True, verbose_name="Заголовки")
    summary = models.TextField(verbose_name="Описание")
    content = models.TextField(verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True)
    published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, verbose_name="Автор")
    like = models.ManyToManyField(Author, related_name='like', blank=True)
    dislike = models.ManyToManyField(Author, related_name='dislike', blank=True)
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def add_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title, model_type='articles')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]


class Comment(models.Model, Rating):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_comments',
                               null=True, blank=True)
    is_child = models.BooleanField(default=False)
    like = models.ManyToManyField(Author, related_name='like_comment', blank=True)
    dislike = models.ManyToManyField(Author, related_name='dislike_comment', blank=True)

    def __str__(self):
        return f'{self.id}. {self.user.username} - {self.article.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]
