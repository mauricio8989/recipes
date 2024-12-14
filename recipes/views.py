from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.core.paginator import Paginator
from utils.pagination import make_pagination_range

PER_PAGE = 9


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(recipes, PER_PAGE)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        int(current_page)
    )

    return render(request, 'recipes/pages/home.html', context={
        "recipes": page_obj,
        "pagination_range": pagination_range,
        "current_page": current_page,
        "page_title": "Home | Recipes"})


def category(request, category_id):
    recipes = Recipe.objects.filter(category__id=category_id, is_published=True).order_by("-id")  # noqa: E501

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(recipes, PER_PAGE)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        int(current_page)
    )
    if not recipes:
        return render(request, 'recipes/pages/404.html', status=404)

    return render(request, 'recipes/pages/category.html', context={
        "recipes": page_obj,
        "pagination_range": pagination_range,
        "current_page": current_page,
        "title": f"{recipes[0].category.name}-Category | "})


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        "recipe": recipe,
        "title": f"{recipe.title}",
        "is_detail_page": True})


def search(request):
    search_item = request.GET.get('q', '').strip()
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_item) |
            Q(description__icontains=search_item)
        ),
        is_published=True,
        ).order_by("-id")  # noqa: E501

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(recipes, PER_PAGE)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        int(current_page)
    )

    if not search_item:
        return render(request, 'recipes/pages/404.html', status=404)
    else:
        return render(request, 'recipes/pages/search.html', {
            'page_title': f'Search for "{search_item}"',
            'search_term': search_item,
            "recipes": page_obj,
            "pagination_range": pagination_range,
            "current_page": current_page,
        })
