from django.contrib import admin

# Register your models here.
from .models import Category, Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'slug', 'preparation_time', 'preparation_time_unit')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe)