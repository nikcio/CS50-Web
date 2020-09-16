from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class Bid(models.Model):
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Listing(models.Model):
    image = models.URLField(max_length=1084, blank=True)
    description = models.CharField(max_length=1084)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField()
    starting_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="listing_start", null=True)
    current_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="listing_current", null=True, blank=True)

    CATEGORIES = {
        ("Fashion", "Fashion"),
        ("Toys", "Toys"),
        ("Electronics", "Electronics"),
        ("Home", "Home"),
        ("Other", "Other")
    }

    category = models.CharField(max_length=64, choices=CATEGORIES, default="Other")
    active = models.BooleanField(default=True)


class Comment(models.Model):
    content = models.CharField(max_length=1084)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)


class WatchList(models.Model):
    listings = models.ManyToManyField(Listing, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
