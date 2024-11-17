from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class TestRecipeModel(RecipeTestBase):

    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_creation(self):
        self.recipe.title = 'This is a test recipe to make sure it works' * 4
        self.assertRaises(ValidationError, self.recipe.full_clean)
