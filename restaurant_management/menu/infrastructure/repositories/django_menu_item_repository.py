from decimal import Decimal
from typing import List, Optional
from core.cache.django_cache_manager import CacheManager
from ...core.domain.entities.menu_item import MenuItem
from ...core.repositories.menu_item_repository import MenuItemRepository
from ...models import MenuItemModel
from ...core.mappers.menu_item_mapper import MenuItemMapper
from core.exceptions.custom_exceptions import EntityNotFoundException

MENU_ITEM_CACHE_PREFIX = "MENU_ITEM_"
MENU_ITEM_ALL_CACHE_PREFIX = "MENU_ITEM_ALL"

class DjangoMenuItemRepository(MenuItemRepository):
      def __init__(self):
         self.cache_manager = CacheManager(MENU_ITEM_CACHE_PREFIX)
         super().__init__()
      
      def get_all(self) -> List[MenuItem]:
         menu_items_cache = self._get_query_set_from_cache()
         if menu_items_cache or len(menu_items_cache) > 0:
            return menu_items_cache

         menu_items = MenuItemModel.objects.all().order_by('id')
         menu = [MenuItemMapper.to_domain(model) for model in menu_items]
         
         return menu
     
      def get_by_id(self, item_id: int, raise_expection=False) -> Optional[MenuItem]:
         menu_item_cache = self._get_by_id_cache(item_id)
         if menu_item_cache:
            return menu_item_cache
         
         return self._get_by_id_db(item_id, raise_expection)
      
      def search(self, filter_params : dict) -> List[MenuItem]:
         pass

      def save(self, menu_item: MenuItem) -> MenuItem:
         if not menu_item.id:
            return self._create(menu_item)

         self._update(menu_item) 
     
      def _create(self, menu_item: MenuItem) -> MenuItem:
         new_item_model = MenuItemMapper.to_model(menu_item)
         
         new_item_model.save()
         
         menu_item_entity = MenuItemMapper.to_domain(new_item_model)

         new_cache_key = self.cache_manager.get_cache_key(menu_item_entity.id)
         self.cache_manager.set(new_cache_key, menu_item)
         self._refresh_query_set_cache()
         
         return menu_item

      def delete(self, item_id: int) -> None:
         MenuItemModel.objects.filter(id=item_id).delete()
         
         cache_key = self.cache_manager.get_cache_key(item_id)
         self.cache_manager.delete(cache_key)  
         self._refresh_query_set_cache()


      def _get_by_id_cache(self, item_id: int) -> Optional[MenuItem]:
         item_cache_key = self.cache_manager.get_cache_key(item_id)
         return self.cache_manager.get(item_cache_key)
 
      def _get_by_id_db(self, item_id: int, raise_expection=False) -> Optional[MenuItem]:
         try:   
            model = MenuItemModel.objects.get(id=item_id)
            return MenuItemMapper.to_domain(model)
         except MenuItemModel.DoesNotExist:
            if raise_expection:
               raise EntityNotFoundException('Menu Item', item_id)
            else:
               return None
         
      def _get_query_set_from_cache(self) -> List[MenuItem]:
         menu_items_cache = self.cache_manager.get(MENU_ITEM_ALL_CACHE_PREFIX)
         if menu_items_cache or len(menu_items_cache) > 0:
            return [MenuItemMapper.to_domain(model) for model in menu_items_cache]

      def _get_query_set_from_cache(self) -> List[MenuItem]:
         menu_items_cache = self.cache_manager.get(MENU_ITEM_ALL_CACHE_PREFIX)
         if menu_items_cache or len(menu_items_cache) > 0:
            return [MenuItemMapper.to_domain(model) for model in menu_items_cache]