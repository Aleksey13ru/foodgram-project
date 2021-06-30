from django import forms
from rest_framework.exceptions import ValidationError

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['image', 'title', 'description', 'tags', 'cooking_time']
        widgets = {'tags': forms.CheckboxSelectMultiple(), }
