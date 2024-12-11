from dependency_injector import containers, providers
from restaurant.repository.table_respository import TableRepository
from restaurant.repository.ingredient_repository import IngredientRepository
from restaurant.services.ingredient_service import IngredientService
from restaurant.services.table_service import TableService
from restaurant.services.ingredient_service import IngredientService


class Container(containers.DeclarativeContainer):
    table_repository = providers.Singleton(TableRepository)
    ingredient_repository = providers.Singleton(IngredientRepository)

    table_service = providers.Factory(TableService, table_repository=table_repository)
    ingredient_service = providers.Factory(IngredientService, ingredient_repository)