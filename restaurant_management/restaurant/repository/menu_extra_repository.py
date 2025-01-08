from restaurant.services.domain.menu_extra import MenuExtraDomain
from restaurant.repository.models.models import MenuExtraModel
from restaurant.mappers.menu_extra_mappers import MenuExtraMapper
from restaurant.repository.common_repository import CommonRepository
from typing import List, Optional

class MenuExtraRepository(CommonRepository[MenuExtraDomain]):
     def __init__(self):
        self.menu_item = MenuExtraModel


     def get_all(self) -> List[MenuExtraDomain]:
        menu_items = self.menu_item.objects.all().order_by('id')
        menu = [
            MenuExtraMapper.to_domain(model)
            for model in menu_items
        ]
        
        return menu
     

     def get_by_id(self, item_id: int) -> Optional[MenuExtraDomain]:
        model = self.menu_item.objects.filter(id=item_id).first()
        if model:
           return MenuExtraMapper.to_domain(model)


     def create(self, menu_item: MenuExtraDomain) -> MenuExtraDomain:
         new_item_model = MenuExtraMapper.to_model(menu_item)
         
         new_item_model.save()

         return MenuExtraMapper.to_domain(new_item_model)


     def update(self,  menu_item: MenuExtraDomain) -> Optional[MenuExtraDomain]:
         pass


     def delete(self, item_id: int) -> bool:
        deleted, _ = self.menu_item.objects.filter(id=item_id).delete()
        return deleted > 0
