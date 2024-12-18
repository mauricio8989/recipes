from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipesSearchViewsTest(RecipeTestBase):

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

    def test_recipe_searche_can_find_recipes_by_title(self):
        title1 = 'Tis is the recipe one'
        title2 = 'Tis is the recipe two'
        recipe1 = self.make_recipe(
            title=title1,
            slug=title1,
            author_data={'username': title1}
        )
        recipe2 = self.make_recipe(
            title=title2,
            slug=title2,
            author_data={'username': title2}
        )
        url_search = reverse('recipes:search')
        response1 = self.client.get(f'{url_search}?q={title1}')
        response2 = self.client.get(f'{url_search}?q={title2}')
        response_both = self.client.get(f'{url_search}?q=Tis')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
