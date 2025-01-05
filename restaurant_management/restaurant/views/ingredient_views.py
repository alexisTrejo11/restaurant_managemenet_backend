from restaurant.utils.response import ApiResponse
from restaurant.serializers import IngredientSerializer, IngredientInsertSerializer
from restaurant.services.ingredient_service import IngredientService
from restaurant.injector.app_module import AppModule
from rest_framework.viewsets import ViewSet
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

container = Injector([AppModule()])

class IngredientViews(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_ingredient_service(self):
        return container.get(IngredientService)

    @swagger_auto_schema(
        operation_description="Get an ingredient by its ID",
        responses={
            200: IngredientSerializer,
            404: "Ingredient not found"
        }
    )
    def get_ingredient_by_id(self, request, ingredient_id):
        ingredient_service = self.get_ingredient_service()

        ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
        if ingredient is None:
            return ApiResponse.not_found('ingredient', 'ID', ingredient_id)

        ingredient_data = IngredientSerializer(ingredient).data
        return ApiResponse.found(ingredient_data, 'Ingredient', 'ID', ingredient_id)


    @swagger_auto_schema(
        operation_description="Get all ingredients",
        responses={
            200: IngredientSerializer(many=True),
        }
    )
    def get_all_ingredients(self, request):
        ingredient_service = self.get_ingredient_service()
        ingredients = ingredient_service.get_all_ingredients()
        ingredients_data = IngredientSerializer(ingredients, many=True).data
        return ApiResponse.ok(ingredients_data, 'Ingredients successfully fetched')


    @swagger_auto_schema(
        operation_description="Create a new ingredient",
        request_body=IngredientInsertSerializer,
        responses={
            201: IngredientSerializer,
            400: "Invalid data"
        }
    )
    def create_ingredient(self, request):
        ingredient_service = self.get_ingredient_service()
        serializer = IngredientInsertSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        ingredient = ingredient_service.create_ingredient(request.data)
        ingredients_data = IngredientSerializer(ingredient).data
        return ApiResponse.created(ingredients_data, 'Ingredient successfully created')


    @swagger_auto_schema(
        operation_description="Delete an ingredient by its ID",
        responses={
            200: "Ingredient successfully deleted",
            404: "Ingredient not found"
        }
    )
    def delete_ingredient_by_id(self, request, ingredient_id):
        ingredient_service = self.get_ingredient_service()
        is_deleted = ingredient_service.delete_ingredient(ingredient_id)
        if not is_deleted:
            return ApiResponse.not_found('Ingredient', 'ID', ingredient_id)

        return ApiResponse.ok(None, f'Ingredient with ID {ingredient_id} successfully deleted')
