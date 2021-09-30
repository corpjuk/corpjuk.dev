from django.db import models
from django.conf import settings
from django.urls import reverse
import pint

from .utils import number_str_to_float
from .validators import validate_unit_of_measure

# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    directions = models.TextField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"id": self.id })
    

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    quantity = models.CharField(max_length=50)
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure]) #lbs, oz, gram, etc
    directions = models.TextField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.absolute_url()

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        print(measurement)
        return measurement #.to_base_units()


    # We can create a conversion function to any unit
    # we just need a try/catch to make sure it can convert.

    # def to_ounces(self):
    #     m = self.convert_to_system()
    #     return m.to('ounces')

    def as_mks(self):
        # meter, kilogram, second
        measurement = self.convert_to_system(system="mks")
        print (measurement)
        return measurement.to_base_units()

    def as_imperial(self):
        #miles, pounds, seconds
        measurement = self.convert_to_system(system='imperial')
        print (measurement)
        return measurement.to_base_units()
        #return measurement.to('pounds')

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