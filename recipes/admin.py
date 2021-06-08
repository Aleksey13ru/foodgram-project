from django.contrib import admin
from .models import Ingredient, Recipe, IngredientRecipe, User, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    search_fields = ('title',)
    list_filter = ('title',)


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredient.through
    extra = 2


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title')
    search_fields = ('title',)
    list_filter = ('author', 'title')
    inlines = (IngredientRecipeInLine,)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(User)
admin.site.register(Tag)
