import random # imports random which has randint(), use this for random int
from django.http import HttpResponse
from django.shortcuts import render
from articles.models import Article
from django.template.loader import render_to_string
from django.shortcuts import render

def home_view(request, id=None, *args, **kwargs):
    context = {'article': Article.objects.all(),}
    return render(request, 'home-view.html', context)

