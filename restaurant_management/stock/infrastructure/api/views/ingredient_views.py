# Django
from core.response.django_response import DjangoResponseWrapper
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from ..serializers.serializers import IngredientSerializer, IngredientInsertSerializer

# Application
from ....application.use_case.ingredient_use_case import (
    GetAllIngredientsUseCase,
    GetIngredientsByIdUseCase,
    CreateIngredientUseCase,
    UpdateIngredientUseCase,
    DeleteIngredientUseCase
)

# Inject
from core.injector.stock_container import IngredientContainer
from dependency_injector.wiring import Provide

class IngredientViews(ViewSet):
    def __init__(
            self, 
            get_ingredient_by_id_use_case: GetIngredientsByIdUseCase = Provide[IngredientContainer.get_ingredient_by_id_use_case],
            get_all_ingredient_use_case: GetAllIngredientsUseCase = Provide[IngredientContainer.get_all_ingredient_use_case],
            create_ingredient_use_case: CreateIngredientUseCase = Provide[IngredientContainer.create_ingredient_use_case],
            update_ingredient_use_case: UpdateIngredientUseCase = Provide[IngredientContainer.update_ingredient_use_case],
            delete_ingredient_use_case: DeleteIngredientUseCase = Provide[IngredientContainer.delete_ingredient_use_case],
            **kwargs):
        self.get_ingredient_by_id_use_case = get_ingredient_by_id_use_case
        self.get_all_ingredients_use_case = get_all_ingredient_use_case
        self.create_ingredient_use_case = create_ingredient_use_case
        self.update_ingredient_use_case = update_ingredient_use_case
        self.delete_ingredient_use_case = delete_ingredient_use_case
        super().__init__(**kwargs)

    permission_classes = [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Get an ingredient by its ID",
        responses={
            200: IngredientSerializer,
            404: "Ingredient not found"
        }
    )
    def retrieve(self, request, pk):
        ingredient_data = self.get_ingredient_by_id_use_case.execute(pk)
        
        return DjangoResponseWrapper.found(
            data=ingredient_data.to_dict(), 
            entity='Ingredient', 
            param='ID',
            value=pk
        )

    @swagger_auto_schema(
        operation_description="Get all ingredients",
        responses={
            200: IngredientSerializer(many=True),
        }
    )
    def list(self, request):
        ingredient_list = self.get_all_ingredients_use_case.execute()
        if not ingredient_list or len(ingredient_list) == 0:
            return DjangoResponseWrapper.success(
                data=[], 
                message='No Ingredients Found'
            )   
        
        return DjangoResponseWrapper.found(
            data=[ingredient.to_dict() for ingredient in ingredient_list], 
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
    def create(self, request):
        serializer = IngredientInsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ingredient = self.create_ingredient_use_case.execute(serializer.validated_data)
        
        return DjangoResponseWrapper.created(
            data=ingredient.to_dict(), 
            entity='Ingredient',
        )

    @swagger_auto_schema(
        operation_description="Delete an ingredient by its ID",
        responses={
            200: "Ingredient successfully deleted",
            404: "Ingredient not found"
        }
    )
    def destroy(self, request, pk):
        self.delete_ingredient_use_case.execute(pk)
        return DjangoResponseWrapper.deleted(f'Ingredient')
