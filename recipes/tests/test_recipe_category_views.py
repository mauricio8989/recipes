from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipesCategoryViewsTest(RecipeTestBase):

    def test_category_view_returns_correct_template(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 2}))
        self.assertIs(view.func, views.category)

    def test_category_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 999}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        recipe = self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': recipe.category.id}))  # noqa: E501
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn(needed_title, content)
        self.assertIn('10 minutos', content)
        self.assertIn('5 porções', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse(
            'recipes:category', kwargs={'category_id': recipe.category.id}
        ))
        self.assertEqual(response.status_code, 404)
