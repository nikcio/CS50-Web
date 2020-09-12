from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
import markdown2
from django.http import HttpResponse
from . import util
from django import forms
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "randomPage": util.list_entries()[random.randrange(0, len(util.list_entries()))]
    })


def page(request, page):
    if util.get_entry(page):
        return render(request, "encyclopedia/page.html", {
            "content": markdown2.markdown(util.get_entry(page)),
            "pageTitle": page,
            "randomPage": util.list_entries()[random.randrange(0, len(util.list_entries()))]
        })
    else:
        return HttpResponse("404 Page not found")


def search(request):
    search_query = request.GET.get('q', None)
    if util.get_entry(search_query):
        return redirect('encyclopedia:page', page=search_query)
    else:
        return render(request, 'encyclopedia/search.html', {
            "entries": [entry for entry in util.list_entries() if search_query in entry.lower()],
            "randomPage": util.list_entries()[random.randrange(0, len(util.list_entries()))]
        })


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        if util.get_entry(title):
            raise ValidationError("Title must be unique")

        return cleaned_data


def new_page(request):
    if request.method == "GET":
        return render(request, 'encyclopedia/newPage.html', {
            "form": NewEntryForm(),
            "randomPage": util.list_entries()[random.randrange(0, len(util.list_entries()))]
        })
    elif request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data['title'],
                            "# " + form.cleaned_data['title'] + '\r\n' + form.cleaned_data['content'])
            return redirect('encyclopedia:page', page=form.cleaned_data['title'])
        else:
            return render(request, 'encyclopedia/newPage.html', {
                "form": form,
                "randomPage": util.list_entries()[random.randrange(0, len(util.list_entries()))]
            })
    else:
        return HttpResponse("404 Page not found")


class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


def edit_page(request, page):
    if request.method == "GET":
        return render(request, 'encyclopedia/editPage.html', {
            "form": EditEntryForm(initial={'content': util.get_entry(page)}),
            "page": page,
            "randomPage": util.list_entries()[random.randrange(0, len(util.list_entries()))]
        })
    elif request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            util.save_entry(page, form.cleaned_data['content'])
            return redirect('encyclopedia:page', page=page)
        else:
            return render(request, 'encyclopedia/editPage.html', {
                "form": form,
                "page": page,
                "randomPage": util.list_entries()[random.randrange(0, len(util.list_entries()))]
            })
    else:
        return HttpResponse("404 Page not found")
