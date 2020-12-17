from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class Index(LoginRequiredMixin, ListView):
    template_name = "webapp/Home.html"


class EditorsHome(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "webapp/EditorHome.html"
