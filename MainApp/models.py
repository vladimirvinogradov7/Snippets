from django.db import models
import datetime
from django.contrib.auth.models import User

LANG_CHOICE = [
    ('py', 'python'),
    ('cpp', 'C++'),
    ('js', 'javascript'),
]


class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANG_CHOICE, default="py")
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(default=datetime.datetime.now)
    public = models.BooleanField(default=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)