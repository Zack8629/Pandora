from django.db import models

from account.models import Author


class Category(models.Model):
    """Defining articles categories"""
    title = models.CharField(max_length=150, db_index=True, verbose_name="Заголовки категорий")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "категории"
        ordering = ["title"]


class Articles(models.Model):
    """We create articles with the necessary fields and categories"""
    title = models.CharField(max_length=150, db_index=True, verbose_name="Заголовки")
    content = models.TextField(verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True)
    published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    author = models.ForeignKey(Author, on_delete=models.PROTECT, verbose_name="Автор")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]
