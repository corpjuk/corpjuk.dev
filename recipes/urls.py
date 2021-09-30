from django.urls import path

from .views import (
    recipe_list_view,
    recipe_detail_view,
    recipe_create_view,
    recipe_update_view
)

app_name='recipes' # recipes:list
urlpatterns = [
    path("", recipe_list_view, name='list'),
    path("create/", recipe_create_view, name='create'),
    path("<int:id>/edit/", recipe_update_view, name='update'),
    path("<int:id>/", recipe_detail_view, name='detail'),
]