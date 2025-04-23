from restaurant.services.domain.menu_extra import MenuExtraDomain
from ...models import MenuExtraModel
from ...core.mappers.menu_item_mapper import MenuExtraMapper
from core.repository.common_repository import CommonRepository
from typing import List

class DjangoMenuExtraRepository(CommonRepository[MenuExtraDomain]):
      def __init__(self):
        self.menu_item = MenuExtraModel

      def get_all(self) -> List[MenuExtraDomain]:
        menu_items = self.menu_item.objects.all().order_by('id')
        menu = [MenuExtraMapper.to_domain(model) for model in menu_items]
        return menu
     
      def get_by_id(self, item_id: int) -> MenuExtraDomain:
         try:
            model = self.menu_item.objects.get(id=item_id)
            return MenuExtraMapper.to_domain(model)
         except MenuExtraModel.DoesNotExist:
            raise ValueError('Menu Extra Not Found')

      def save(self, menu_item : MenuExtraDomain) -> MenuExtraDomain:
         if not menu_item.id:
            return self._create(menu_item)
         
         return self._update(menu_item)

      def _create(self, menu_item : MenuExtraDomain) -> MenuExtraDomain:
         new_item_model = MenuExtraMapper.to_model(menu_item)
         
         new_item_model.save()

         return MenuExtraMapper.to_domain(new_item_model)

      def _update(self,  menu_item: MenuExtraDomain) -> MenuExtraDomain:
         pass

      def delete(self, item_id: int) -> None:
         self.menu_item.objects.filter(id=item_id).delete()
