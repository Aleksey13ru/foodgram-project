from django.db.models import Sum


def get_tags(request):
    """ Получаем теги """
    all_tags = ['breakfast', 'lunch', 'dinner']
    tags = []
    for tag in all_tags:
        if request.GET.get(tag) == 'True':
            tags.append(tag)
    if not tags:
        tags = all_tags
    return tags


def get_ingredients(request):
    """ Получаем ингредиенты"""
    ingredients = {}
    for key, name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[name] = int(request.POST[f'valueIngredient_{_[1]}'])
    return ingredients


def ingredients_for_pdf(request):
    """ Получаем ингредиенты для выгрузки pdf"""
    ingredients = (request.user.basket.order_by('ingredient__title').
                   values('ingredient__title', 'ingredient__dimension').
                   annotate(amount=Sum('recipe_ingredient__value')).all())
    ingredients_list = []
    for ingredient in ingredients:
        string = (f'{ingredient["ingredient__title"]} '
                  f'({ingredient["ingredient__dimension"]}) '
                  f'— {ingredient["amount"]}')
        ingredients_list.append(string)
    return ingredients_list


def check_ingredients_value(ingredients):
    """Проверка на то, что количество всех ингредиентов больше 0"""
    for ing_amount in ingredients.values():
        if int(ing_amount) <= 0:
            return True
        return False


def validate_ingredients(form, ingredients):
    """Валидация ингредиентов"""
    if check_ingredients_value(ingredients):
        context = {'form': form,
                   'ingr_error':
                       'Вы ввели отрицательное число ингредиентов'}
        return context
