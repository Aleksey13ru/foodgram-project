import io

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .models import Recipe, Ingredient, IngredientRecipe, User
from .forms import RecipeForm


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


def index(request):
    """Главная страница"""
    tags = get_tags(request)
    recipe_list = Recipe.objects.filter(tags__name__in=tags).\
        order_by('-pub_date').distinct()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/indexAuth.html', {'page': page,
                                                      'tags': tags
                                                      })


def profile(request, username):
    """Профиль автора"""
    tags = get_tags(request)
    author = get_object_or_404(User, username=username)
    recipe_records = Recipe.objects.filter(author=author, tags__name__in=tags).\
        order_by('-pub_date').distinct()
    paginator = Paginator(recipe_records, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/authorRecipe.html',
                  {'author': author,
                   'page': page,
                   'paginator': paginator,
                   'recipe_records': recipe_records}
                  )


@login_required
def new_recipe(request):
    """Функция для создания рецепта"""
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    ingredients = get_ingredients(request)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        for title, value in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            ingredient_recipe = IngredientRecipe(recipe=recipe,
                                                 ingredient=ingredient,
                                                 value=value)
            ingredient_recipe.save()
        form.save_m2m()
        return redirect('index')
    return render(request, 'recipes/formRecipe.html', {'form': form})


def recipe_view(request, username, recipe_id):
    """Функция для просмотра рецепта"""
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    return render(request, 'recipes/singlePage.html', {'author': recipe.author,
                                                       'recipe': recipe,
                                                       })


@login_required
def recipe_edit(request, username, recipe_id):
    """Функция для редактирования рецепта"""
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    if request.user != recipe.author:
        return redirect('index')
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
    ingredients = get_ingredients(request)
    if form.is_valid():
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        for item in ingredients:
            IngredientRecipe(recipe=recipe,
                             ingredient=Ingredient.objects.get(title=f'{item}'),
                             value=ingredients[item])
        form.save_m2m()
        return redirect('index')
    return render(request, 'recipes/formRecipe.html', {'form': form,
                                                       'recipe': recipe, })


@login_required
def recipe_delete(request, username, recipe_id):
    """Функция для удаления рецепта"""
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')


@login_required
def favorites_recipe(request):
    """Функция страницы, куда будут выведены рецепты,
    которые текущий пользователь добавил в избранное"""
    tags = get_tags(request)
    recipe_list = request.user.favorites.filter(tags__name__in=tags).distinct()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/favorite.html', {'page': page,
                                                     'paginator': paginator})


@login_required
def my_follow(request):
    """Функция страницы, куда будут выведены авторы,
    на которых подписался текущий пользователь"""
    my_follow_list = request.user.follow.all().order_by('-authors').distinct()
    paginator = Paginator(my_follow_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/myFollow.html', {'page': page,
                                                     'paginator': paginator})


@login_required
def shopping_list(request):
    """Функция для создания списка покупок"""
    shop_list = request.user.basket.all()
    return render(request, 'recipes/shopList.html', {'shop_list': shop_list, })


@login_required
def shopping_list_download(request):
    """Функция для выгрузки pdf файла списка ингредиентов"""
    ingredients = request.user.basket.order_by('ingredient__title').\
        values('ingredient__title', 'ingredient__dimension').\
        annotate(amount=Sum('recipe_ingredient__value')).all()

    ingredients_list = []
    for ingredient in ingredients:
        string = (f'{ingredient["ingredient__title"]} '
                  f'({ingredient["ingredient__dimension"]}) '
                  f'— {ingredient["amount"]}')
        ingredients_list.append(string)

    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    p = canvas.Canvas(buffer)
    p.setFont('FreeSans', 12)
    y = 800
    for line in ingredients_list:
        p.drawString(50, y, line)
        y -= 10
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename='Cписок покупок.pdf')


def page_not_found(request, exception):
    return render(request, "404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "500.html", status=500)
