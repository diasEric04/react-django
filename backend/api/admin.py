from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'slug'
    list_display_links = 'id',
    search_fields = 'id', 'title', 'slug'
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',)
    }
