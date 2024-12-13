from restaurant.services.domain.menu_item import MenuItem
from restaurant.repository.models.models import MenuItemModel
from restaurant.mappers.menu_item_mappers import MenuItemMapper
from restaurant.repository.common_repository import CommonRepository
from typing import List, Optional


class MenuItemRepository(CommonRepository[MenuItem]):
     def __init__(self):
        self.menu_item = MenuItemModel

     def get_all(self) -> List[MenuItem]:
        menu_items = self.menu_item.objects.all().order_by('id')
        menu = [
            MenuItemMapper.map_model_to_domain(model)
            for model in menu_items
        ]
        
        return menu


     def get_by_id(self, item_id: int) -> Optional[MenuItem]:
        model = self.menu_item.objects.filter(id=item_id).first()
        if model:
           return MenuItemMapper.map_model_to_domain(model)
        return None


     def create(self, menu_item: MenuItem) -> MenuItem:
         new_item_model = MenuItemMapper.map_domain_to_model(menu_item)
         
         new_item_model.save()

         return MenuItemMapper.map_model_to_domain(new_item_model)


     def update(self,  menu_item: MenuItem) -> Optional[MenuItem]:
         pass


     def delete(self, item_id: int) -> bool:
        deleted, _ = self.menu_item.objects.filter(id=item_id).delete()
        return deleted > 0
