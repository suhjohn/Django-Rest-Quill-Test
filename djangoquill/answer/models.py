from bs4 import BeautifulSoup
from django.conf import settings
from django.db import models

from djangorestquill.models import QuillPost

__all__ = (
    'Answer',
)


class Answer(models.Model):
    title = models.CharField(max_length=100, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    quillpost = models.OneToOneField(QuillPost, on_delete=models.CASCADE)

    def __str__(self):
        return f'title: {self.title}, content: {self.quillpost}'


