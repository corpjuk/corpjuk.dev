
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from django.forms.models import modelformset_factory

# The model form for query sets - that's what modelformset_factory is
# Take this instance of a model form and turn it into a bunch of instances
# It creates a Formset class
# Model Form Functions docs
# https://docs.djangoproject.com/en/3.2/ref/forms/models/

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient
# Create your views here.
# CRUD Views -> Create Retrieve Update & Delete

@login_required()
def recipe_list_view(request):
    # .all is not right here
    qs = Recipe.objects.filter(user=request.user)
    context = {
        'object_list': qs 
    }
    return render(request, "recipes/list.html", context)

@login_required()
def recipe_detail_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    context = {
        'object': obj
    }
    return render(request, "recipes/detail.html", context)

@login_required()
def recipe_create_view(request, ):
    form = RecipeForm(request.POST or None)
    context = {'form': form }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context)

@login_required()
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)

    # Model Form Functions
    # https://docs.djangoproject.com/en/3.2/ref/forms/models/
    # docs
    # Formset = modelformset_factory(Model, form=RecipeIngredientForm, extra=0)

    RecipeIngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0)
    qs = obj.recipeingredient_set.all() # [] could be empty queryset
    formset = RecipeIngredientFormset(request.POST or None, queryset=qs)
    context = {
        'form': form,
        'formset': formset,
        'object': obj
    }

    # checking is all conditions are true seperated by commas
    # The primary task of a Form object is to validate data. 
    # With a bound Form instance, call the is_valid() method to run validation and return a boolean designating whether the data was valid:
    # https://docs.djangoproject.com/en/3.2/ref/forms/api/

    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)  # commit=False means it wnn't save
        parent.save()
        # formset.save() can also be used directly
        for form in formset:
            child = form.save(commit=False)
            # without child.recipe = parent, will get a NOT NULL constraint failed
            # The recipe model cannot be null for an ingredient so it has a Not Null constraint
            if child.recipe is None:
                print("Added new")
                child.recipe = parent
            child.recipe = parent
            child.save()

        context['message'] = 'Data saved.'
    return render(request, "recipes/create-update.html", context)
   
 

     

        

        # child = form_2.save(commit=False) #not actually saving
        # child.recipe = parent
        # child.save()

        # print("form", form.cleaned_data)
        # print("form_2", form_2.cleaned_data)
        # obj = form.save()
        
    
