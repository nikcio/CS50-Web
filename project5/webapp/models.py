from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    isEditor = models.BooleanField(default=False)
    saved = models.ManyToManyField('Media', blank=True)


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
    editor = models.ForeignKey(User, on_delete=models.CASCADE)

    def serialize(self, request_user):
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "trailerUrl": self.trailerUrl,
            "date": self.date,
            "description": self.description,
            "image": self.image.url,
            "isSeries": self.isSeries,
            "seasons": self.seasons,
            "createDate": self.createDate,
            "editor": self.editor.id,
            "saved": request_user.saved.filter(id=self.id).exists()
        }
