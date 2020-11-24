from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    isEditor = models.BooleanField()
    Saved = models.ManyToManyField('Media')


class Media(models.Model):
    title = models.TextField(max_length=255)
    genre = models.TextField(max_length=255)
    trailerUrl = models.URLField(max_length=1084)
    date = models.DateField()
    description = models.TextField(max_length=512)
    image = models.ImageField()
    isSeries = models.BooleanField()
    seasons = models.IntegerField(null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    Editor = models.ForeignKey(User, on_delete=models.CASCADE)
