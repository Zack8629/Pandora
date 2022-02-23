from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(AbstractUser):
    email = models.EmailField(verbose_name='email', unique=True)
    about_me = models.TextField(verbose_name="обо мне", blank=True)
    birthday = models.DateField(verbose_name='день рождения', blank=True, null=True)
