"""
To render pages
"""


import random # imports random which has randint(), use this for random int
from django.http import HttpResponse
from articles.models import Article
from django.template.loader import render_to_string
from django.shortcuts import render

#from django.random import randint


#name = Justin
#HTML_STRING = f"""<h1>Hello {name}<h1>"""

######

#  home_view is the main page

######



def home_view(request, id=None, *args, **kwargs):
    #random_id = random.randint(1,4)
    article_obj = Article.objects.get(id=2)
    article_queryset = Article.objects.all()
    my_list = article_queryset #[123, 456, 789]
    

    #article_title = article_obj.title
    #article_content = article_obj.content
    context = {

                'object_list': article_queryset,
                'my_list': my_list,
                'title': article_obj.title,
                'id': article_obj.id,
                'content': article_obj.content
            }


    # H1_STRING = """<h1>{title}! ({id})</h1> 
    #             <p>{content}!</p>
    #             """.format(**context)
    HTML_STRING = render_to_string("home-view.html", context=context)

    return HttpResponse(HTML_STRING)
from django.shortcuts import render
def home(request):
	return render(request, "home.html")
