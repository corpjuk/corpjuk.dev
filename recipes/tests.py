from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import RecipeIngredient, Recipe

# https://www.youtube.com/watch?v=c48rGz1EfFk
# 52 - Understanding Relationships between Models via Tests

User = get_user_model()

#Not going to use in the long run, just showing how to set up Data with UserTestCase
#Probably want to test for validation in the future here
#The created user in UserTestCase and RecipeTestCase are isolated to its own testcase.

# I need to understand how assertTrue, assertEqual work
# 

class UserTestCase(TestCase):
    def setUp(self):
        #built in user class .create_user which is unique to the User class.
        self.user_a = User.objects.create_user('corpjuk', password='abc123')
    
    def test_user_pw(self):
        checked = self.user_a.check_password("abc123")
        self.assertTrue(checked)

# The Recipe Test Case is used to test the Recipe Model

class RecipeTestCase(TestCase):

    #this is the setUp function where we set up the test database
    def setUp(self):
        #built in user class .create_user which is unique to the User class.
        self.user_a = User.objects.create_user('corpjuk', password='abc123')
        #above is how you create a user

        
        #below is how to create an object. And we need to use the required fields from Models. Name and User.
        self.recipe_a = Recipe.objects.create(
            name = 'Chana Masala',
            user = self.user_a
        )
        self.recipe_b = Recipe.objects.create(
            name = 'Roasted Broccoli',
            user = self.user_a
        )

        #now lets create a recipe_ingredient
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe = self.recipe_a,
            name='Chickpeas',
            quantity='1/2',
            unit='pound',
        )
    
    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)
        #print(qs.count)

    #this function is testing if there is a qs.count and it's 1.
    # it is 1 because we created a recipe_a in setUp

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs=user.recipe_set.all()
        # don't forget qs=self.user_a.recipe_set.all() is the same thing

        # _set gives a query set
        
        #print(qs)
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs=Recipe.objects.filter(user=user)        
        #print(qs)
        self.assertEqual(qs.count(), 2)

    # Next we're going to test Recipe Ingredient count
    # To see if we're creating the Ingredient Object Model

    def test_user_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs=recipe.recipeingredient_set.all()
        #print(qs)
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_ingredient_forward_count(self):
        recipe = self.recipe_a
        qs=RecipeIngredient.objects.filter(recipe=recipe)
        #print(qs)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation(self):
        user = self.user_a
        qs = RecipeIngredient.objects.filter(recipe__user=user)
        print(qs)
        self.assertEqual(qs.count(), 1)

    # a two level reverse relationship is not something done often
    # You can have more levels than this 3 levels, 4 levels, etc
    # as long as there is a foreign key at the top I assume which is the User

    # three levels would look like
    # RecipeIngredientImage.objects.filter(recipeingredient__recipe__user=user)

    # reverse relationships can get complicated

    def test_user_two_level_relation_reverse(self):
        user = self.user_a
        recipeingredient_ids = list(user.recipe_set.all().values_list('recipeingredient__id', flat=True))
        qs = RecipeIngredient.objects.filter(id__in=recipeingredient_ids)
        print(recipeingredient_ids)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list('id', flat=True)
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids)
        #print(qs)
        self.assertEqual(qs.count(), 1)
    
    # I tried to write a test_recipe_case without creating the Recipe.objects.create()
    # def test_recipe_case(TestCase):
    #     qs = Recipe.objects.all()
    #     print(qs)
    # this returned an empty qs []
