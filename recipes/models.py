import pint
import pathlib
import uuid
from django.conf import settings
from django.db.models import Q, Count
from django.db import models
from django.urls import reverse
from .utils import number_str_to_float
from .validators import validate_unit_of_measure

"""
- Global
    - Ingredients
    - Recipes
- User
    - Ingredients
    - Recipes
        - Ingredients
        - Directions for Ingredients
"""


class RecipeQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return (
                self.none()
            )  # this is the same as Article.objects.none(), but it's still an empty list []
        lookups = (
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(directions__icontains=query)
        )
        return self.filter(lookups)

    # def get_previous(self, recipe):
    #     return self.filter(id__lt=recipe.id).order_by('-id').first()

    # def get_next(self, recipe):
    #     return self.filter(id__gt=recipe.id).order_by('id').first()

    # def get_previous_hx_url(self, recipe):
    #     previous_recipe = self.get_previous(recipe)
    #     if previous_recipe:
    #         return previous_recipe.get_hx_url()
    #     return None

    # def get_next_hx_url(self, recipe):
    #     next_recipe = self.get_next(recipe)
    #     if next_recipe:
    #         return next_recipe.get_hx_url()
    #     return None


class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    # def all(self):
    #     return self.get_queryset().filter(published=True)

    def all(self, qs=None):
        if qs is None:
            qs = self.get_queryset()
        return qs

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    # Get previous and next recipes
    # def get_previous(self, recipe):
    #     return (
    #         self.get_queryset()
    #         .filter(created__lt=recipe.created)
    #         .order_by("-created")
    #         .first()
    #     )

    # def get_next(self, recipe):
    #     return (
    #         self.get_queryset()
    #         .filter(created__gt=recipe.created)
    #         .order_by("created")
    #         .first()
    #     )

    # def get_previous_hx_url(self, recipe):
    #     previous = self.get_previous(recipe)
    #     if previous is not None:
    #         return previous.get_hx_url()

    # def get_next_hx_url(self, recipe):
    #     next = self.get_next(recipe)
    #     if next is not None:
    #         return next.get_hx_url()


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-timestamp"]

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"id": self.id})

    def get_hx_url(self):
        return reverse("recipes:hx-detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("recipes:update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("recipes:delete", kwargs={"id": self.id})

    def get_ingredients_children(self):
        return self.recipeingredient_set.all()

    def get_previous_hx_url(self):
        previous_recipe = Recipe.objects.filter(
            user=self.user, timestamp__lt=self.timestamp
        ).last()
        if previous_recipe:
            return reverse("recipes:hx-detail", args=[previous_recipe.id])
        return None

    def get_next_hx_url(self):
        next_recipe = Recipe.objects.filter(
            user=self.user, timestamp__gt=self.timestamp
        ).first()
        if next_recipe:
            return reverse("recipes:hx-detail", args=[next_recipe.id])
        return None

    def get_previous_by_created(self):
        return self.get_previous_by_field("created")

    def get_next_by_created(self):
        return self.get_next_by_field("created")


def recipe_ingredient_image_upload_handler(instance, filename):
    # grabbing file extention
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1())  # uuid1 -> uuid + timestamps
    return f"static/recipes/ingredient{new_fname}{fpath.suffix}"


class RecipeIngredientImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=recipe_ingredient_image_upload_handler
    )  # stores path to the file
    # image
    # extracted_text


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)  # 1 1/4
    quantity_as_float = models.FloatField(blank=True, null=True)
    # pounds, lbs, oz, gram, etc
    unit = models.CharField(
        max_length=50, validators=[validate_unit_of_measure]
    )
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

    def get_delete_url(self):
        kwargs = {"parent_id": self.recipe.id, "id": self.id}
        return reverse("recipes:ingredient-delete", kwargs=kwargs)

    def get_hx_edit_url(self):
        kwargs = {"parent_id": self.recipe.id, "id": self.id}
        return reverse("recipes:hx-ingredient-detail", kwargs=kwargs)

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        return measurement  # .to_base_units()

    def as_mks(self):
        # meter, kilogram, second
        measurement = self.convert_to_system(system="mks")
        return measurement.to_base_units()

    def as_imperial(self):
        # miles, pounds, seconds
        measurement = self.convert_to_system(system="imperial")
        return measurement.to_base_units()

    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)


# class RecipeImage():
#     recipe = models.ForeignKey(Recipe)
