from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self')
    likes = models.ManyToManyField('Post', related_name="likers")

    def serialize(self):
        return {
            "username": self.username
        }


class Post(models.Model):
    likes = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self, request_user):
        return {
            "likes": self.likes,
            "user": self.user.username,
            "content": self.content,
            "liked": request_user.likes.filter(id=self.id).exists(),
            "id": self.id,
            "time": self.timestamp.strftime("%m-%d-%Y %H:%M%p"),
            "userid": self.user.id,
            "following": request_user.following.filter(id=request_user.id).exists()
        }

    def serialize_ano(self):
        return {
            "likes": self.likes,
            "user": self.user.username,
            "content": self.content,
            "liked": "ano",
            "id": self.id,
            "time": self.timestamp.strftime("%m-%d-%Y %H:%M%p"),
            "userid": self.user.id,
            "following": "ano"
        }
