from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipe, User, Ingredient
from .serializers import IngredientsSerializer


class PurchaseViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        recipe = Recipe.objects.get(id=int(request.data['id']))
        if recipe:
            request.user.basket.add(recipe)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})

    def delete(self, request,  *args, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        if recipe_id:
            recipe = Recipe.objects.get(id=recipe_id)
            request.user.basket.remove(recipe)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})


class FavoriteViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        recipe = Recipe.objects.get(id=int(request.data['id']))
        if recipe:
            request.user.favorites.add(recipe)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})

    def delete(self, request,  *args, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        if recipe_id:
            recipe = Recipe.objects.get(id=recipe_id)
            request.user.favorites.remove(recipe)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})


class SubscriptionViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        author_id = request.data.get('id')
        if author_id:
            author = User.objects.get(id=author_id)
            request.user.follow.add(author)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})

    def delete(self, request,  *args, **kwargs):
        author_id = kwargs.get('user_id')
        if author_id:
            author = User.objects.get(id=author_id)
            request.user.follow.remove(author)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_ingredients(request):
    query = request.GET.get('query')
    if query is not None:
        ingredients = Ingredient.objects.filter(title__startswith=query)
        serializer = IngredientsSerializer(ingredients, many=True)
        return JsonResponse(serializer.data, safe=False,
                            json_dumps_params={'ensure_ascii': False})
    return Response({'error': 'query is empty'})
