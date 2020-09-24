from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, WatchList, CATEGORIES


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
    image = forms.URLField(max_length=1084,
                           widget=forms.TextInput({'placeholder': 'https://imagehoster.com/image.png'}))
    description = forms.CharField(max_length=1084, required=True,
                                  widget=forms.TextInput({'placeholder': 'Text here...'}))
    title = forms.CharField(max_length=255, required=True, widget=forms.TextInput({'placeholder': 'Title...'}))
    close_date = forms.DateTimeField(required=True, input_formats=['%Y-%m-%d'])
    starting_bid = forms.IntegerField(required=True, widget=forms.TextInput({'placeholder': '100'}))
    category = forms.ChoiceField(required=True, choices=CATEGORIES)


def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            start_bid = Bid.objects.create(amount=form.cleaned_data["starting_bid"], user=request.user)
            start_bid.save()
            new_listing = Listing.objects.create(image=form.cleaned_data["image"],
                                                 description=form.cleaned_data["description"],
                                                 title=form.cleaned_data["title"],
                                                 user=request.user, close_date=form.cleaned_data["close_date"],
                                                 starting_bid=start_bid, current_bid=start_bid,
                                                 category=form.cleaned_data["category"])
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))
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
        "watchlist_id": get_watch_id(request),
        "watchlist_user": WatchList.objects.get(pk=get_watch_id(request))
    })


def watchlist(request, watchlist_id):
    return render(request, "auctions/watchlist.html", {
        "watchlist": WatchList.objects.get(pk=watchlist_id),
        "watchlist_id": get_watch_id(request),
        "listings": WatchList.objects.get(pk=get_watch_id(request)).listings.filter(active=True)
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "watchlist_id": get_watch_id(request),
        "items": ["Fashion", "Toys", "Electronics", "Home", "Other"],
        "category_icons": ["ion:shirt", "whh:teddybear", "jam:computer-f", "dashicons:admin-home", "jam:inboxes"],
    })


def category(request, category_name):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True, category=category_name),
        "watchlist_id": get_watch_id(request)
    })


def add_watchlist(request, listing_id):
    if request.method == "POST":
        _watchlist = WatchList.objects.get(pk=get_watch_id(request))
        _watchlist.listings.add(Listing.objects.get(pk=listing_id))
        _watchlist.save()
        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))
    else:
        return HttpResponseRedirect(reverse('index'))
