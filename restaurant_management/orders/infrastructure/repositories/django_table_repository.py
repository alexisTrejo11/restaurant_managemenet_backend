from typing import List, Optional
from ..models.table_model import TableModel
from reservations.domain.entities.table import Table
from core.cache.django_cache_manager import CacheManager
from core.exceptions.custom_exceptions import EntityNotFoundException
from ...core.mappers.table_mappers import TableMapper
from ...core.repositories.table_repository import TableRepository

TABLE_CACHE_PREFIX = "TABLE_"
TABLE_ALL_CACHE_PREFIX = "TABLE_ALL"

class DjangoTableRepository(TableRepository):
    def __init__(self):
        self.cache_manager = CacheManager(TABLE_CACHE_PREFIX)

    def get_all(self) -> List[Table]:
        """
        Retrieve all tables, checking the cache first.
        
        Returns:
            List[Table]: A list of all tables.
        """
        tables_cache = self._get_query_set_from_cache()
        if tables_cache:
            return tables_cache

        models = TableModel.objects.all().order_by('id')
        tables_list = [TableMapper.model_to_domain(model) for model in models]

        self.cache_manager.set(TABLE_ALL_CACHE_PREFIX, tables_list)

        return tables_list

    def get_by_id(self, id: int, raise_exception=False) -> Optional[Table]:
        """
        Retrieve a table by its id, checking the cache first.
        
        Args:
            id (int): The id of the table to retrieve.
        
        Returns:
            Optional[Table]: The retrieved table, or None if not found.
        """
        table_cache = self._get_by_id_cache(id)
        if table_cache:
            return table_cache

        return self._get_by_id_db(id, raise_exception)

    def save(self, table: Table) -> Table:
        if not table.id:
            return self._create(table)
        
        return self._update(table)
    
    def delete(self, id: int) -> bool:
        """
        Delete a table from the database and cache.
        
        Args:
            id (int): The id of the table to delete.
        
        Returns:
            bool: True if the table was deleted, False otherwise.
        """
        deleted, _ = TableModel.objects.filter(id=id).delete()

        cache_key = self.cache_manager.get_cache_key(id)
        self.cache_manager.delete(cache_key)
        self._refresh_query_set_cache()

        return deleted > 0

    def set_as_available(self, id: int) -> None:
        """
        Set a table as available in the database and cache.
        
        Args:
            id (int): The id of the table to update.
        """
        table_model = TableModel.objects.filter(id=id).first()
        if table_model:
            table_model.is_available = True
            table_model.save()

            cache_key = self.cache_manager.get_cache_key(id)
            self.cache_manager.set(cache_key, TableMapper.model_to_domain(table_model))
            self._refresh_query_set_cache()

    def set_as_unavailable(self, id: int) -> None:
        """
        Set a table as unavailable in the database and cache.
        
        Args:
            id (int): The id of the table to update.
        """
        table_model = TableModel.objects.filter(id=id).first()
        if table_model:
            table_model.is_available = False
            table_model.save()

            cache_key = self.cache_manager.get_cache_key(id)
            self.cache_manager.set(cache_key, TableMapper.model_to_domain(table_model))
            self._refresh_query_set_cache()

    def _create(self, table: Table) -> Table:
        """
        Create a new table and save it to the database and cache.
        
        Args:
            table (Table): The table entity to create.
        
        Returns:
            Table: The created table.
        """
        model = TableModel.objects.create(
            id=table.id,
            capacity=table.capacity,
            is_available=table.is_available
        )

        created_table = TableMapper.model_to_domain(model)

        cache_key = self.cache_manager.get_cache_key(created_table.id)
        self.cache_manager.set(cache_key, created_table)
        self._refresh_query_set_cache()

        return created_table

    def _update(self, table: Table) -> Table:
        """
        Update an existing table in the database and cache.
        
        Args:
            table (Table): The table entity to update.
        
        Returns:
            Table: The updated table.
        """
        try:
            existing_table_model = TableModel.objects.get(id=table.id)
        except TableModel.DoesNotExist:
            raise EntityNotFoundException("Table", table.id)

        existing_table_model.capacity = table.capacity
        existing_table_model.is_available = table.is_available
        existing_table_model.save()

        table_updated = TableMapper.model_to_domain(existing_table_model)

        cache_key = self.cache_manager.get_cache_key(table_updated.id)
        self.cache_manager.set(cache_key, table_updated)
        self._refresh_query_set_cache()

        return table_updated


    def _get_by_id_cache(self, id: int) -> Optional[Table]:
        """
        Retrieve a table by its id from the cache.
        
        Args:
            id (int): The id of the table to retrieve.
        
        Returns:
            Optional[Table]: The cached table, or None if not found.
        """
        cache_key = self.cache_manager.get_cache_key(id)
        return self.cache_manager.get(cache_key)

    def _get_by_id_db(self, id: int, raise_exception=False) -> Optional[Table]:
        """
        Retrieve a table by its id from the database.
        """
        try:
            table_model = TableModel.objects.get(id=id)
            return TableMapper.model_to_domain(table_model)
        except TableModel.DoesNotExist:
            if raise_exception:
                raise EntityNotFoundException("Table", id)
            return None

    def _get_query_set_from_cache(self) -> Optional[List[Table]]:
        """
        Retrieve all tables from the cache.
        
        Returns:
            Optional[List[Table]]: A list of cached tables, or None if not found.
        """
        tables_cache = self.cache_manager.get(TABLE_ALL_CACHE_PREFIX)
        if tables_cache:
            return [TableMapper.model_to_domain(model) for model in tables_cache]
        return None

    def _refresh_query_set_cache(self):
        """
        Refresh the cache for all tables.
        """
        models = TableModel.objects.all().order_by('id')
        tables_list = [TableMapper.model_to_domain(model) for model in models]
        self.cache_manager.set(TABLE_ALL_CACHE_PREFIX, tables_list)