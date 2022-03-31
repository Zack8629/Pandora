from account.models import Author
from articles.models import Articles, Comment


def like_dislike_rating(obj, user, likes, dislikes):
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


type_object = {
    'article': Articles.objects.get,
    'comment': Comment.objects.get

}


def like_dislike(type_obj, username, pk, likes, dislikes):
    user = Author.objects.get(username=username)
    object = type_object[type_obj](pk=pk)
    like_dislike_rating(object, user, likes, dislikes)
