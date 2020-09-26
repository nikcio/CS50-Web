from django.contrib import admin
from . import models


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'listing']


class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'current_bid', 'category', 'user', 'active']


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user']


class BidAdmin(admin.ModelAdmin):
    list_display = ['amount', 'user', 'date']


# Register your models here.
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Listing, ListingAdmin)
admin.site.register(models.WatchList, WatchlistAdmin)
admin.site.register(models.Bid, BidAdmin)
admin.site.register(models.User)
