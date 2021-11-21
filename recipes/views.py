from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory # model form for querysets
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient
# CRUD -> Create Retrieve Update & Delete

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "object_list": qs
    }
    return render(request, "recipes/list.html", context)


@login_required
def recipe_detail_view(request, id=None):
    hx_url = reverse("recipes:hx-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "recipes/detail.html", context) 

@login_required
def recipe_detail_hx_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is  None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "recipes/partials/detail.html", context) 



@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context)  

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    print(obj)
    form = RecipeForm(request.POST or None, instance=obj)
    # Formset = modelformset_factory(Model, form=ModelForm, extra=0)
    RecipeIngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0)
    qs = obj.recipeingredient_set.all() # []
    formset = RecipeIngredientFormset(request.POST or None, queryset=qs)
    context = {
        "form": form,
        "formset": formset,
        "object": obj
    }
    print(form.is_valid())
    print(form.errors.as_json())
    print(formset.is_valid())
    print(form.errors.as_json())
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        # formset.save()
        for form in formset:
            child = form.save(commit=False)
            child.recipe = parent
            print(child)
            child.save()
        context['message'] = 'Data saved.'
    if request.htmx:
    #if request.META.get("HTTP_HX_REQUEST") != 'true':
        return render(request, "recipes/partials/forms.html", context)
    return render(request, "recipes/create-update.html", context) 




# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect, render, get_object_or_404

# from django.forms.models import modelformset_factory

# # The model form for query sets - that's what modelformset_factory is
# # Take this instance of a model form and turn it into a bunch of instances
# # It creates a Formset class
# # Model Form Functions docs
# # https://docs.djangoproject.com/en/3.2/ref/forms/models/

# from .forms import RecipeForm, RecipeIngredientForm
# from .models import Recipe, RecipeIngredient
# # Create your views here.
# # CRUD Views -> Create Retrieve Update & Delete

# @login_required()
# def recipe_list_view(request):
#     # .all is not right here
#     qs = Recipe.objects.filter(user=request.user)
#     context = {
#         'object_list': qs 
#     }
#     return render(request, "recipes/list.html", context)

# @login_required()
# def recipe_detail_view(request, id=None):
#     obj = get_object_or_404(Recipe, id=id, user=request.user)
#     context = {
#         'object': obj
#     }
#     return render(request, "recipes/detail.html", context)

# @login_required()
# def recipe_create_view(request, ):
#     form = RecipeForm(request.POST or None)
#     context = {'form': form }
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = request.user
#         obj.save()
#         return redirect(obj.get_absolute_url())
#     return render(request, "recipes/create-update.html", context)

# @login_required()
# def recipe_update_view(request, id=None):
#     obj = get_object_or_404(Recipe, id=id, user=request.user)
#     form = RecipeForm(request.POST or None, instance=obj)

#     # no longer need form_2 with RecipeIngredientFormset
#     # form_2 = RecipeIngredientForm(request.POST or None)

#     # Model Form Functions
#     # https://docs.djangoproject.com/en/3.2/ref/forms/models/
#     # docs
#     # Formset = modelformset_factory(Model, form=RecipeIngredientForm, extra=0)

#     RecipeIngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0)
#     qs = obj.recipeingredient_set.all() # [] could be empty queryset
#     formset = RecipeIngredientFormset(request.POST or None, queryset=qs)
#     context = {
#         'form': form,
#         #'form_2': form_2,
#         'formset': formset,
#         'object': obj
#     }
#     # if request.method == "POST":
#     #     print(request.POST)
#     # checking is all conditions are true seperated by commas
#     # The primary task of a Form object is to validate data. 
#     # With a bound Form instance, call the is_valid() method to run validation and return a boolean designating whether the data was valid:
#     # https://docs.djangoproject.com/en/3.2/ref/forms/api/

#     # if all checks all to be true instead of using a bunch of if statements
#     # if all([form.is_valid(), form_2.is_valid(), formset.is_valid()]):
#     if all([form.is_valid(), formset.is_valid()]):
#         parent = form.save(commit=False)  # commit=False means it wnn't save
#         parent.save()

#         # child.recipe = parent
#         # formset.save() can also be used directly
#         for form in formset:
#             child = form.save(commit=False)
#             # without child.recipe = parent, will get a NOT NULL constraint failed
#             # The recipe model cannot be null for an ingredient so it has a Not Null constraint
#             child.recipe = parent
#             child.save()
#         context['message'] = 'Data saved.'
#     if request.htmx:
#         return render(request, "recipes/partials/forms.html", context)
#     return render(request, "recipes/create-update.html", context)
   
 

     

        

        # child = form_2.save(commit=False) #not actually saving
        # child.recipe = parent
        # child.save()

        # print("form", form.cleaned_data)
        # print("form_2", form_2.cleaned_data)
        # obj = form.save()
        
    
