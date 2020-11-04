from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    likes = models.ManyToManyField('Post', related_name="likers")

    def serialize(self):
        return {
            "username": self.username
        }


class Follower(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = ('follower', 'following')


class Post(models.Model):
    likes = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self, request_user):
        output = {
            "likes": self.likes,
            "user": self.user.username,
            "content": self.content,
            "id": self.id,
            "time": self.timestamp.strftime("%m-%d-%Y %H:%M%p"),
            "userid": self.user.id
        }
        if request_user.is_authenticated:
            output["following"] = request_user.following.filter(id=request_user.id).exists()
            output["liked"] = request_user.likes.filter(id=self.id).exists()
        return output
