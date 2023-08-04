from django.shortcuts import render


def index(request):
    context = {
        'page_title': 'Home'
    }
    return render(
        request,
        'main/pages/index.html',
        context
    )
