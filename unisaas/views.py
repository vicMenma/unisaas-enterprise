from django.shortcuts import render


def home_view(request):
    return render(request, "home.html")


def login_view(request):
    return render(request, "login.html")


def portal_view(request):
    return render(request, "portal.html")


def dean_portal_view(request):
    return render(request, "dean_portal.html")
