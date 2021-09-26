from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import RecipeIngredient, Recipe

# Register your models here.

User = get_user_model()

# Episode 51
# https://www.youtube.com/watch?v=hpo18rVZhG4
# Admin Inlines for Foreign Keys - Python & Django 3.2 Tutorial Series
# Credit
# https://github.com/jmitchel3

# admin.site.unregister(User)
# # admin.site.register(RecipeIngredient)

# class RecipeInline(admin.StackedInline):
#     model = RecipeIngredient
#     extra = 0

# class UserAdmin(admin.ModelAdmin):
#     inlines = [RecipeInline]
#     list_display = ['username']

# admin.site.register(User, UserAdmin)

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ['quantity_as_float']
    # fields = ['name', 'quantity', 'unit', 'directions',]

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['user', 'name']
    readonly_fields = ['timestamp', 'updated']
    raw_id_fields = ['user']
    #search_fields = ['name', 'description', ]

admin.site.register(Recipe, RecipeAdmin)
