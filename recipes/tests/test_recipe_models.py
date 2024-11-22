from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class TestRecipeModel(RecipeTestBase):

    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = Recipe(
            title='Recipe title',
            description='Recipe description',
            slug='recipe-test-99999',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='porções',
            preparation_steps='recipe preparation steps',
            preparation_steps_is_html=False,
            cover='recipe_cover.jpg',
            author=self.make_author(username='Mauricio'),
            category=self.make_category('category_test')
        )
        return recipe

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))
        self.assertRaises(ValidationError, self.recipe.full_clean)

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        recipe.full_clean()
        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        recipe.full_clean()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing representation'
        self.recipe.full_clean()  # Ensure the fields are valid before comparing with the string representation.  # noqa: E501
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing representation')


class TestCategoryModel(RecipeTestBase):

    def setUp(self):
        self.category = self.make_category(
            name='Category test'
        )
        return super().setUp()

    def test_category_model_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'a' * 70
        self.assertRaises(ValidationError, self.category.full_clean)
