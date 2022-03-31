from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(AbstractUser):
    email = models.EmailField(verbose_name='email', unique=True)
    about_me = models.TextField(verbose_name="обо мне", blank=True)
    birthday = models.DateField(verbose_name='день рождения', blank=True, null=True)
    is_moderator = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=10),
                name="A qty value is valid between 1 and 10",
            )
        ]