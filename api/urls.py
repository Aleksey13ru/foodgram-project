from django.urls import path

from .views import PurchaseViewSet, FavoriteViewSet, SubscriptionViewSet, \
    api_get_ingredients


urlpatterns = [
    path('purchases/', PurchaseViewSet.as_view()),
    path('purchases/<int:recipe_id>/', PurchaseViewSet.as_view()),
    path('favorites', FavoriteViewSet.as_view()),
    path('favorites/<int:recipe_id>/', FavoriteViewSet.as_view()),
    path('subscriptions', SubscriptionViewSet.as_view()),
    path('subscriptions/<int:user_id>/', SubscriptionViewSet.as_view()),
    path('ingredients/', api_get_ingredients, name='api_get_ingredients'),
    ]
