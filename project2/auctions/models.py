from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class Listing(models.Model):
    image = models.ImageField()
    description = models.CharField(max_length=1084)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField()


class Bid(models.Model):
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField(max_length=1084)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
