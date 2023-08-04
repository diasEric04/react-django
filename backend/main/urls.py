from django.urls import path
from .views import index  # type:ignore

app_name = 'main'

urlpatterns = [
    path('', index, name='index')
]
