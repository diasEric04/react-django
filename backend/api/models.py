from django.db import models
from django.contrib.auth.models import User
from utils.rands import slugify_new


class Post(models.Model):
    title = models.CharField(max_length=65)  # precisa
    slug = models.SlugField(  # nao precisa
        unique=True, default='',
        null=False, max_length=255
    )
    description = models.CharField(max_length=125)  # precisa
    created_at = models.DateTimeField(
        auto_now=True
    )
    updated_at = models.DateTimeField(
        auto_now_add=True
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_created_by'
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by'
    )
    content = models.TextField()  # precisa

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 5)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
