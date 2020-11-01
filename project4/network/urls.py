
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("following", views.following, name="following"),
    path("newpost", views.new_post, name="newpost"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like")
]
