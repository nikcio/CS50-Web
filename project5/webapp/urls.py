from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("editor", views.EditorsHome.as_view(), name="editor_home"),
]
