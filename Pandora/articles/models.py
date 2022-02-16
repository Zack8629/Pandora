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
        verbose_name_plural = "категории"
        ordering = ["title"]


class Articles(models.Model):
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
