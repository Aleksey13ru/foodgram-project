from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['image', 'title', 'description', 'tags', 'cooking_time']
        widgets = {'tags': forms.CheckboxSelectMultiple(), }
