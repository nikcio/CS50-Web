from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.page, name="page"),
    path("search", views.search, name="search"),
    path("new-page", views.new_page, name="newPage"),
    path("edit-page/<str:page>", views.edit_page, name="editPage"),
]
