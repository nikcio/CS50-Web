from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, WatchList


def get_watch_id(request):
    if request.user.is_authenticated:
        try:
            return WatchList.objects.get(user=request.user).id
        except WatchList.DoesNotExist:
            new_watchlist = WatchList.objects.create(user=request.user).id
            return new_watchlist
    else:
        return None


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True),
        "watchlist_id": get_watch_id(request)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class CreateListingForm(forms.Form):
    image = forms.URLField(max_length=1084)
    description = forms.CharField(max_length=1084)
    title = forms.CharField(max_length=255)
    close_date = forms.DateTimeField()
    starting_bid = forms.IntegerField()


def create_listing(request):
    if request.method == "POST":
        form = request.POST
        if form.is_valid():
            start_bid = Bid.objects.create(amount=form["starting_bid"], user=request.user)
            start_bid.save()
            new_listing = Listing.objects.create(image=form["image"], description=form["description"],
                                                 title=form["title"],
                                                 user=request.user, close_date=form["close_date"],
                                                 starting_bid=start_bid, current_bid=start_bid)
            new_listing.save()
            return HttpResponseRedirect("index")
        else:
            return render(request, "auctions/create.html", {
                "form": form,
                "watchlist_id": get_watch_id(request)
            })

    else:
        return render(request, "auctions/create.html", {
            "form": CreateListingForm(),
            "watchlist_id": get_watch_id(request)
        })


def listing(request, listing_id):
    try:
        _listing = Listing.objects.get(pk=int(listing_id))
    except Listing.DoesNotExist:
        return Http404("Listing not found")

    return render(request, "auctions/listing.html", {
        "listing": _listing,
        "comments": _listing.comments.all(),
        "watchlist_id": get_watch_id(request)
    })


def watchlist(request, watchlist_id):
    return render(request, "auctions/watchlist.html", {
        "watchlist": WatchList.objects.get(pk=watchlist_id),
        "watchlist_id": get_watch_id(request)
    })