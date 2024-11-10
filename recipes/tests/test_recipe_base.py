from django.test import TestCase  # noqa: E261
from recipes.models import Recipe, Category, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_category(self, name='category123'):
        return Category.objects.create(name=name)

    def make_author(
            self, first_name='John',
            last_name='Smith',
            username='johnsmith',
            email='john.smith@example.com',
            password='password123'):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password)

    def make_recipe(
            self,
            title='Recipe title',
            description='Recipe description',
            slug='recipe-title',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='porções',
            preparation_steps='recipe preparation steps',
            preparation_steps_is_html=False,
            is_published=True,
            cover='recipe_cover.jpg',
            author_data=None,
            category_data=None):
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}
        return Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            cover=cover,
            author=self.make_author(**author_data),
            category=self.make_category(**category_data))
