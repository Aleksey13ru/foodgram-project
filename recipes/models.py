from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    title = models.CharField(max_length=256,
                             verbose_name='Название')
    dimension = models.CharField(max_length=64,
                                 verbose_name='Единицы измерения')

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='authors',
                               verbose_name='Автор публикации (пользователь)')
    title = models.CharField(max_length=256, verbose_name='Название')
    image = models.ImageField(upload_to='recipe_image/',
                              verbose_name='Картинка', blank=True)
    description = models.TextField(verbose_name='Текстовое описание')
    ingredient = models.ManyToManyField(Ingredient, through='IngredientRecipe',
                                        verbose_name='Ингредиенты')
    in_favorites = models.ManyToManyField(User, related_name='favorites',
                                          verbose_name='Избранное',
                                          blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='Тег',
                                  related_name='recipes')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления')
    in_basket = models.ManyToManyField(User, related_name='basket',
                                       verbose_name='Корзина покупок',
                                       blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.title


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredient_recipe')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredient')
    value = models.IntegerField()
