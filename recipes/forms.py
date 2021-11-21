from django import forms

from .models import Recipe, RecipeIngredient

# https://docs.djangoproject.com/en/3.2/ref/forms/widgets/
# Read Docs - Important
# There are third party solutions to help with repetitiveness

class RecipeForm(forms.ModelForm):
    required_css_class = 'required-field'
    #css class use hyphens
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    # help_text is outside the widget
    name = forms.CharField(help_text='This is your help! <a href="/contact">Contact us</a>')
    #name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Recipe Name", })), help_text='This is the help text!')
    # description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
            new_data = {
                "placeholder": f'Recipe {str(field)}',
                "class": 'form-control'
            }
            # str(field) = 'name', 'description', 'directions'
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        # default widget 
        # self.name['name'].label = ''
        #self.fields['name'].widget.attrs.update({'class': 'form-control-2'})
        self.fields['description'].widget.attrs.update({'rows': '2'})
        self.fields['directions'].widget.attrs.update({'rows': '4'})

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']