import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return JsonResponse([post.serialize(request.user) for post in posts], safe=False)
    else:
        posts = Post.objects.all()
        return JsonResponse([post.serialize_ano() for post in posts], safe=False)


def following(request):
    following = request.user.following.all()
    return JsonResponse([follow_user.serialize() for follow_user in following], safe=False)


@csrf_exempt
@login_required
def new_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    post = Post(user=request.user, likes=0, content=data.get("content"))
    post.save()

    return JsonResponse({"message": "Post added successfully."}, status=201)


@csrf_exempt
def like(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        data = json.loads(request.body)
        if data.get("like"):
            request.user.likes.add(post)
            return HttpResponse(status=204)
        else:
            request.user.likes.remove(post)
            return HttpResponse(status=204)

    return JsonResponse({
        "error": "GET or PUT request required."}, status=400)


@csrf_exempt
def follow(request, user_id):
    if request.method == "PUT":
        user = User.objects.get(pk=user_id)
        data = json.loads(request.body)
        if data.get("follow"):
            request.user.following.add(user)
            return HttpResponse(status=204)
        else:
            request.user.following.remove(user)
            return HttpResponse(status=204)

    return JsonResponse({
        "error": "GET or PUT request required."}, status=400)
