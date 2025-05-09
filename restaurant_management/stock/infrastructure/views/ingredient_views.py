from core.response.django_response import DjangoResponseWrapper
from restaurant.serializers import IngredientSerializer, IngredientInsertSerializer
from core.injector.app_module import AppModule
from rest_framework.viewsets import ViewSet
from injector import Injector
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from ...application.use_case.ingredient_use_case import (
    GetAllIngredientsUseCase,
    GetIngredientsByIdUseCase,
    CreateIngredientUseCase,
    UpdateIngredientUseCase,
    DeleteIngredientUseCase
)

container = Injector([AppModule()])

class IngredientViews(ViewSet):
    def __init__(self, **kwargs):
        self.get_ingredient_by_id_use_case = container.get(GetIngredientsByIdUseCase)
        self.get_all_ingredients_use_case = container.get(GetAllIngredientsUseCase)
        self.create_ingredient_use_case = container.get(CreateIngredientUseCase)
        self.update_ingredient_use_case = container.get(UpdateIngredientUseCase)
        self.delete_ingredient_use_case = container.get(DeleteIngredientUseCase)
        super().__init__(**kwargs)

    permission_classes = [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Get an ingredient by its ID",
        responses={
            200: IngredientSerializer,
            404: "Ingredient not found"
        }
    )
    def retrieve(self, request, ingredient_id):
        ingredient_data = self.get_ingredient_by_id_use_case.execute(ingredient_id)
        
        return DjangoResponseWrapper.found(
            data=ingredient_data, 
            entity='Ingredient', 
            param='ID',
            value=ingredient_id
        )


    @swagger_auto_schema(
        operation_description="Get all ingredients",
        responses={
            200: IngredientSerializer(many=True),
        }
    )
    def list(self, request):
        ingredients_data = self.get_all_ingredients_use_case.execute()
        return DjangoResponseWrapper.found(
            data=ingredients_data, 
            entity='All Ingredients'
        )


    @swagger_auto_schema(
        operation_description="Create a new ingredient",
        request_body=IngredientInsertSerializer,
        responses={
            201: IngredientSerializer,
            400: "Invalid data"
        }
    )
    def create(self, request, stock_id):
        serializer = IngredientInsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ingredient = self.create_ingredient_use_case.execute(**serializer.validated_data)
        
        ingredients_data = IngredientSerializer(ingredient).data
        return DjangoResponseWrapper.created(ingredients_data, 'Ingredient successfully created')


    @swagger_auto_schema(
        operation_description="Delete an ingredient by its ID",
        responses={
            200: "Ingredient successfully deleted",
            404: "Ingredient not found"
        }
    )
    def destroy(self, request, ingredient_id):
        self.delete_ingredient_use_case.execute(ingredient_id)
        return DjangoResponseWrapper.no_content(f'Ingredient with ID {ingredient_id} successfully deleted')
