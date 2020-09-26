from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, WatchList, CATEGORIES, Comment


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
                           widget=forms.TextInput({'placeholder': 'https://imagehoster.com/image.png'}),
                           required=False)
    description = forms.CharField(max_length=1084, required=True,
                                  widget=forms.TextInput({'placeholder': 'Text here...'}))
    title = forms.CharField(max_length=255, required=True, widget=forms.TextInput({'placeholder': 'Title...'}))
    close_date = forms.DateTimeField(required=True, input_formats=['%Y-%m-%d'])
    starting_bid = forms.IntegerField(required=True, widget=forms.TextInput({'placeholder': '100'}))
    category = forms.ChoiceField(required=True, choices=CATEGORIES)


@login_required
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

    _message = "";

    if request.method == "POST":
        if int(request.POST["amount"]) > _listing.current_bid.amount:
            _bid = Bid.objects.create(user=request.user, amount=request.POST["amount"])
            _bid.save()
            _listing.current_bid = _bid
            _listing.save()
        else:
            _message = "Your bid is lower than current bid"

    return render(request, "auctions/listing.html", {
        "listing": _listing,
        "comments": _listing.comments.all(),
        "watchlist_id": get_watch_id(request) if request.user.is_authenticated else "",
        "watchlist_user": WatchList.objects.get(pk=get_watch_id(request)) if request.user.is_authenticated else "",
        "message": _message
    })


@login_required
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


@login_required
def add_watchlist(request, listing_id):
    if request.method == "POST":
        _watchlist = WatchList.objects.get(pk=get_watch_id(request))
        _watchlist.listings.add(Listing.objects.get(pk=listing_id))
        _watchlist.save()
        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))
    else:
        return HttpResponseRedirect(reverse('index'))


@login_required
def remove_watchlist(request, listing_id):
    if request.method == "POST":
        _watchlist = WatchList.objects.get(pk=get_watch_id(request))
        _watchlist.listings.remove(Listing.objects.get(pk=listing_id))
        _watchlist.save()
        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))
    else:
        return HttpResponseRedirect(reverse('index'))


@login_required
def close_listing(request, listing_id):
    try:
        _listing = Listing.objects.get(pk=int(listing_id))
    except Listing.DoesNotExist:
        return Http404("Listing not found")

    if request.method == "POST" and request.user == _listing.user:
        _listing.active = False
        _listing.save()
        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))
    else:
        return HttpResponseRedirect(reverse('index'))


@login_required
def add_comment(request, listing_id):
    try:
        _listing = Listing.objects.get(pk=int(listing_id))
    except Listing.DoesNotExist:
        return Http404("Listing not found")

    if request.method == "POST":
        _comment = Comment.objects.create(content=request.POST["comment"], user=request.user, listing=_listing)
        _comment.save()
        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))
    else:
        return HttpResponseRedirect(reverse('index'))
