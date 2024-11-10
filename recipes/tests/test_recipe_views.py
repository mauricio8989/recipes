from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipesViewsTest(RecipeTestBase):

    def test_home_view_returns_correct_template(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_category_view_returns_correct_template(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 2}))
        self.assertIs(view.func, views.category)

    def test_recipe_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe title', content)
        self.assertIn('10 minutos', content)
        self.assertIn('5 porções', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_view_returns_404_if_recipes_not_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 999}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_detail_view_returns_correct_template(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 3}))
        self.assertIs(view.func, views.recipe)

    def test_home_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 999}))  # noqa: E501
        self.assertEqual(response.status_code, 404)

    def test_home_view_returns_status_code_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('Nenhum receita cadastrada ainda 🥲.', response.content.decode('utf-8'))  # noqa: E501
