from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import ArticleForm



# Create your views here.


def article_detail_view(request, slug=None, *args, **kwargs):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except  Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
            # a little confused why it gets set to first
        except:
            raise Http404
    context = {
        "object": article_obj,
    }
    return render(request, "articles/detail.html", context=context)


def article_search_view(request):
    #print(dir(request))
    #print(request.GET)
    query_dict = request.GET # this is a dictionary
    #query = query_dict.get("q") # <input type='text' name='q' />

    try:
        query = int(query_dict.get("q"))
    except:
        query = None
    #article_obj = None
    qs = Article.objects.all()
    if query is not None:
        #article_obj = Article.objects.get(id=query)
        qs = Article.objects.filter(title__icontains=query)
    context = {
        # "object": article_obj,
        "object_list": qs
    }
    return render(request, "articles/search.html", context=context)

#@csrf_exempt Security Risk. We can use this decorator to circumvent the csrf token requirment. Useful for building REST API.

@login_required
def article_create_view(request):
    #print(request.POST)
    form = ArticleForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        article_object = form.save()
        context['form'] = ArticleForm()
        return redirect(article_object.get_absolute_url())
        # A different way to do the return redirect
        # return redirect("article-detail", slug=article_object.slug)
        # context['object'] = article_object
        # context['created'] = True
    return render(request, "articles/create.html", context=context)

# def article_create_view(request):
#     #print(request.POST)
#     form = ArticleForm()
#     context = {
#         "form": form,
#     }
#     if request.method == "POST":
#         form = ArticleForm(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data.get("title")
#             content = form.cleaned_data.get("content")
#             # title = request.POST.get("title")
#             # content = request.POST.get("content")
#             article_object = Article.objects.create(title=title, content=content)
#             context['object'] = article_object
#             context['created'] = True
    
#     return render(request, "articles/create.html", context=context)