from django.shortcuts import redirect, render
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import ArticleForm


# Create your views here.


def article_list_view(request):
    qs = Article.objects.all()
    context = {"articles": qs}
    if request.htmx:
        print("htmx request from article_list_view" + str(context))
        return render(request, "articles/partials/detail.html", context)
    else:
        print("normal request from article_list_view" + str(context))
        return render(request, "articles/articles.html", context)


def article_detail_view(request, slug=None, *args, **kwargs):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
    context = {
        "object": article_obj,
    }
    if request.htmx:
        print("htmx request from article_detail_view" + str(context))
        return render(
            request, "articles/partials/detail.html", context=context
        )
    else:
        print("normal request from article_detail_view" + str(context))
        return render(request, "articles/articles.html", context=context)


# clean version #things to learn print(dir(request)), print(request.GET), qs = Article.objects.search(query), query = request.GET.get('q')
def article_search_view(request):
    query = request.GET.get("q")  # this is a dictionary
    qs = Article.objects.search(query=query)
    context = {"object_list": qs}
    if query == None:
        context = {
            "article": Article.objects.all(),
        }
        return render(request, "articles/articles.html", context=context)
    else:
        return render(request, "articles/search.html", context=context)


# @csrf_exempt Security Risk. We can use this decorator to circumvent the csrf token requirment. Useful for building REST API.


@login_required
def article_create_view(request):
    # print(request.POST)
    form = ArticleForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        article_object = form.save()
        context["form"] = ArticleForm()
        return redirect(article_object.get_absolute_url())
    return render(request, "articles/create.html", context=context)
