from django.contrib import admin
from django.db.models import Count

from .models import Ingredient, IngredientRecipe, Recipe, Tag, User


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    search_fields = ('title',)
    list_filter = ('title',)


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredient.through
    extra = 2
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'favorite_count')
    search_fields = ('title',)
    list_filter = ('author', 'title')
    inlines = (IngredientRecipeInLine,)

    def favorite_count(self, obj):
        return obj.in_favorites.count()

    favorite_count.short_description = "Избранное"


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(User)
admin.site.register(Tag)
