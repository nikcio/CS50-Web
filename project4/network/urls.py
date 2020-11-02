
from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", views.Posts.as_view(), name="posts"),
    path("following", views.Following.as_view(), name="following"),
    path("newpost", views.new_post, name="newpost"),
    path("user/<int:userid>", views.UserView.as_view(), name="User"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like")
]
