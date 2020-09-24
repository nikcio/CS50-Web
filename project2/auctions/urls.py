from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist/<int:watchlist_id>", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.category, name="category"),
    path("watchlist/add<int:listing_id>", views.add_watchlist, name="add_watchlist"),
]
