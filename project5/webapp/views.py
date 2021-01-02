import json
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse


class Index(LoginRequiredMixin, ListView):
    template_name = "webapp/Home.html"
    model = models.Media
    paginate_by = 10

    def get_queryset(self):
        return models.Media.objects.filter(isSeries=False).order_by("title")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context["new"] = models.Media.objects.filter(isSeries=False).order_by("createDate")[:10]
        context["hero"] = models.Media.objects.filter(isSeries=False).order_by("createDate").first()
        context["moviesPage"] = True
        context["showing"] = "movies"
        context["saved"] = self.request.user.saved.all()
        return context


class Saved(LoginRequiredMixin, ListView):
    template_name = "webapp/Home.html"
    model = models.Media
    paginate_by = 10

    def get_queryset(self):
        return self.request.user.saved.order_by("title")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Saved, self).get_context_data(**kwargs)
        context["new"] = self.request.user.saved.all().order_by("createDate")[:10]
        context["hero"] = self.request.user.saved.all().order_by("createDate").first()
        context["savedPage"] = True
        context["showing"] = "saved"
        context["saved"] = self.request.user.saved.all()
        return context


class Series(LoginRequiredMixin, ListView):
    template_name = "webapp/Home.html"
    model = models.Media
    paginate_by = 10

    def get_queryset(self):
        return models.Media.objects.filter(isSeries=True).order_by("title")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Series, self).get_context_data(**kwargs)
        context["new"] = models.Media.objects.filter(isSeries=True).order_by("createDate")[:10]
        context["hero"] = models.Media.objects.filter(isSeries=True).order_by("createDate").first()
        context["seriesPage"] = True
        context["showing"] = "series"
        context["saved"] = self.request.user.saved.all()
        return context


class ViewTrailer(LoginRequiredMixin, DetailView):
    template_name = "webapp/ViewTrailer.html"
    model = models.Media


class EditorsHome(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "webapp/EditorHome.html"
    model = models.Media
    paginate_by = 10

    def test_func(self):
        return self.request.user.isEditor

    def get_queryset(self):
        return models.Media.objects.filter(isSeries=False).order_by("title")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EditorsHome, self).get_context_data(**kwargs)
        context["saved"] = self.request.user.saved.all()
        return context


class EditorsSeries(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "webapp/EditorSeries.html"
    model = models.Media
    paginate_by = 10

    def test_func(self):
        return self.request.user.isEditor

    def get_queryset(self):
        return models.Media.objects.filter(isSeries=True).order_by("title")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EditorsSeries, self).get_context_data(**kwargs)
        context["saved"] = self.request.user.saved.all()
        return context


class EditorsNewMovie(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "webapp/EditorNewMovie.html"
    model = models.Media
    fields = ["title", "genre", "trailerUrl", "date", "description", "image", "isSeries", "editor"]

    def test_func(self):
        return self.request.user.isEditor


class EditorsNewSeries(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "webapp/EditorNewSeries.html"
    model = models.Media
    fields = ["title", "genre", "trailerUrl", "date", "seasons", "isSeries", "description", "image", "isSeries", "editor"]

    def test_func(self):
        return self.request.user.isEditor


class EditorsEditMovie(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "webapp/EditorEditMovie.html"
    model = models.Media
    fields = ["title", "genre", "trailerUrl", "date", "description", "image", "isSeries", "editor"]

    def test_func(self):
        return self.request.user.isEditor


class EditorsEditSeries(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "webapp/EditorEditSeries.html"
    model = models.Media
    fields = ["title", "genre", "trailerUrl", "date", "seasons", "isSeries", "description", "image", "isSeries",
              "editor"]

    def test_func(self):
        return self.request.user.isEditor


@login_required
@csrf_exempt
def media(request, media_id):
    try:
        mediaItem = models.Media.objects.get(pk=media_id)
    except models.Media.DoesNotExist:
        return JsonResponse({"Error", "Media not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(mediaItem.serialize(request.user))
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("saved") is not None:
            if data.get("saved"):
                request.user.saved.add(mediaItem)
                return HttpResponse(status=204)
            else:
                request.user.saved.remove(mediaItem)
                return HttpResponse(status=204)
        else:
            return JsonResponse({"Error", "Must have liked parameter"}, status=400)
    else:
        return JsonResponse({"Error", "Must be GET request"}, status=400)


@login_required
@csrf_exempt
def delete(request, media_id):
    try:
        mediaItem = models.Media.objects.get(pk=media_id)
    except models.Media.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    mediaItem.delete()
    return HttpResponseRedirect(reverse("index"))