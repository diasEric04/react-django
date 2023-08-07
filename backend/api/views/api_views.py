from api.models import Post
from django.http import JsonResponse


def get(request):
    posts = Post.objects.all()
    data = list(posts.values())
    return JsonResponse(data, safe=False)
