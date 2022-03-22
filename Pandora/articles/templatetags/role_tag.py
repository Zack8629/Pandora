from django import template

from account.models import Author

register = template.Library()


def is_role_user(user):
    if user:
        username_role = Author.objects.filter(username=user).first()
        if username_role:
            if username_role.is_superuser:
                return f'{user} (admin)'
            if username_role.is_moderator:
                return f'{user} (moderator)'
    return user


register.filter('is_role_user', is_role_user)
