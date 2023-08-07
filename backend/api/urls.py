from django.urls import path
from .views import get

app_name = 'api'

urlpatterns = [
    # path('get/<int:id>/', get_unique, name="get_unique"),
    path('get/', get, name="get"),
    # path('post/', post, name='post'),
]
