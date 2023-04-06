import random  # imports random which has randint(), use this for random int
from django.http import HttpResponse
from django.shortcuts import render
from articles.models import Article
from django.template.loader import render_to_string
from django.shortcuts import render


def home_view(request, id=None, *args, **kwargs):
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, "home-view.html", context)


def whyvegan_view(request, id=None, *args, **kwargs):
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, "whyvegan.html", context)


def about_view(request, id=None, *args, **kwargs):
    context = {
        "title": "About Us",
        "description": "We are a 100% vegan recipe website that utilizes the speed of htmx without annoying ads.",
    }
    return render(request, "about.html", context)
