from django.test import TestCase  # noqa: E261
from django.urls import reverse


class RecipeUrlsTest(TestCase):
    def test_recipe_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 2})
        self.assertEqual(url, '/recipes/category/2/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'id': 3})
        self.assertEqual(url, '/recipes/3/')
