from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['image', 'title', 'description', 'tags', 'cooking_time']
        help_texts = {
                      'image': 'Картинка',
                      'title': 'Заголовок',
                      'description': 'Описание',
                      'tags': 'Тэг',
                      'cooking_time': 'Время приготовления',
                      }
        widgets = {'tags': forms.CheckboxSelectMultiple(), }

    def save(self, *args, **kwargs):
        pass

    def clean(self, *args, **kwargs):
        pass
