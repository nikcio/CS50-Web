import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from .models import User, Post, Follower


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("posts"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("posts"))


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
        return HttpResponseRedirect(reverse("posts"))
    else:
        return render(request, "network/register.html")


class Posts(ListView):
    paginate_by = 10
    model = Post
    template_name = 'network/index.html'
    ordering = '-timestamp'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Posts, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["liked"] = self.request.user.likes.all()
        else:
            context["liked"] = None
        return context


class Following(ListView):
    paginate_by = 10
    template_name = 'network/index.html'

    def get_queryset(self):
        return Post.objects.filter(user__in=[item.following for item in self.request.user.following.all()]).order_by('-timestamp')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Following, self).get_context_data(**kwargs)
        context["liked"] = self.request.user.likes.all()
        return context


class UserView(ListView):
    paginate_by = 10
    template_name = 'network/user.html'

    def get_queryset(self):
        return Post.objects.filter(user=User.objects.get(pk=self.kwargs['userid']))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context["userid"] = self.kwargs['userid']
        context["userpage"] = User.objects.get(pk=self.kwargs['userid'])
        context["following"] = any(item in self.request.user.following.all() for item in User.objects.get(pk=self.kwargs['userid']).followers.all())
        context["followers"] = User.objects.get(pk=self.kwargs['userid']).followers.all()
        context["liked"] = self.request.user.likes.all()
        return context


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
@login_required
def update_post(request, pk):
    if request.method != "PUT":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    post = Post.objects.get(pk=pk, user=request.user)
    post.content = data.get("content")
    post.save()

    return JsonResponse({"message": "Post added successfully."}, status=201)


@csrf_exempt
def like(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        data = json.loads(request.body)
        if data.get("like"):
            request.user.likes.add(post)
            post.likes += 1
            post.save()
            print(request.user.likes.count())
            return HttpResponse(status=204)
        else:
            request.user.likes.remove(post)
            post.likes -= 1
            post.save()
            return HttpResponse(status=204)

    return JsonResponse({
        "error": "PUT request required."}, status=400)


@csrf_exempt
def follow(request, user_id):
    if request.method == "PUT":
        user = User.objects.get(pk=user_id)
        data = json.loads(request.body)
        if data.get("follow"):
            request.user.following.add(Follower.objects.create(following=user, follower=request.user))
            return HttpResponse(status=204)
        else:
            Follower.objects.get(following=user, follower=request.user).delete()
            return HttpResponse(status=204)

    return JsonResponse({
        "error": "PUT request required."}, status=400)
