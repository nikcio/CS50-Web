from django.views.generic import FormView
from django.contrib.auth import login, authenticate
from . import forms


class Signup(FormView):
    template_name = 'registration/signup.html'
    form_class = forms.SignUpForm
    success_url = ""

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)
