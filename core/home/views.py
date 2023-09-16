from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    context = {"page": "Home"}
    return render(request, "pages/home.html")


def about(request):
    context = {"page": "About"}
    return render(request, "pages/about.html")
