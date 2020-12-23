from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("series", views.Series.as_view(), name="series"),
    path("saved", views.Saved.as_view(), name="saved"),
    path("trailer/<int:pk>", views.ViewTrailer.as_view(), name="view_trailer"),
    path("editor", views.EditorsHome.as_view(), name="editor_home"),
    path("editor/series", views.EditorsSeries.as_view(), name="editor_series"),
    path("editor/new/movie", views.EditorsNewMovie.as_view(success_url="/editor"), name="editor_new_movie"),
    path("editor/new/series", views.EditorsNewSeries.as_view(success_url="/editor/series"), name="editor_new_series"),
    path("editor/edit/movie/<int:pk>", views.EditorsEditMovie.as_view(success_url="/editor"), name="editor_edit_movie"),
    path("editor/edit/series/<int:pk>", views.EditorsEditSeries.as_view(success_url="/editor/series"), name="editor_edit_series"),
    path("delete/<int:media_id>", views.delete, name="delete"),
    path("get/<int:media_id>", views.media, name="get_media"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
