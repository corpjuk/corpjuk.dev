from django import forms

from .models import Recipe, RecipeIngredient

# https://docs.djangoproject.com/en/3.2/ref/forms/widgets/
# important

class RecipeForm(forms.ModelForm):

    #css class use hyphens
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Recipe Name", }))
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']