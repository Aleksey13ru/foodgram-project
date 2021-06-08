from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('favorite/', views.favorites_recipe, name='favorite'),
    path('follow/', views.my_follow, name='my_follow'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('shopping_list_download/', views.shopping_list_download,
         name='shopping_list_download'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('<str:username>/<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe_edit'),

    # path(<str:username>/<int:recipe_id>/delete/', views.recipe_delete,
    #          name='recipe_delete'),
]
