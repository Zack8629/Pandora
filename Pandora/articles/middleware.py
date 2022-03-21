from .models import Articles


class ViewsArticleMiddleware:
    flag = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        if request.resolver_match is not None:
            if request.resolver_match.url_name == 'article_view':
                if request.method == "GET":
                    slug = request.resolver_match.kwargs.get('slug')
                    if slug:
                        article = Articles.objects.get(slug=slug)
                        article.add_views()

        return response
