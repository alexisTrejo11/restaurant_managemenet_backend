from dependency_injector import containers, providers
from restaurant.repository.table_respository import TableRepository
from restaurant.services.table_service import TableService
from restaurant.views import table_views

class Container(containers.DeclarativeContainer):
    table_repository = providers.Singleton(TableRepository)
    table_service = providers.Factory(TableService, table_repository=table_repository)