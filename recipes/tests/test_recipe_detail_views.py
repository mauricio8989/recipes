from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipesDetailViewsTest(RecipeTestBase):

    def test_detail_view_returns_correct_template(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 3}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a recipe-detail test, it loads just one recipe'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))  # noqa: E501
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': recipe.id}
        ))
        self.assertEqual(response.status_code, 404)

    def test_search_view_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_search_view_returns_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=recipes')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')  # + '?q=recipes'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_scaped(self):
        url = reverse('recipes:search') + '?q=Test'
        response = self.client.get(url)
        self.assertIn('Search for &quot;Test&quot;', response.content.decode('utf-8'))  # noqa: E501
