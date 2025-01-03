from restaurant.repository.menu_item_repository import MenuItemRepository
from restaurant.mappers.menu_item_mappers import MenuItemMapper
from restaurant.services.domain.menu_item import MenuItem
from injector import inject

class MenuItemService:
    @inject
    def __init__(self, menu_repository: MenuItemRepository):
        self.menu_repository = menu_repository

    def get_menu_by_id(self, menu_id) -> MenuItem:
        return self.menu_repository.get_by_id(menu_id)

    def get_all_menus(self) -> list:
        return self.menu_repository.get_all()

    def create_menu(self, serializer_data) -> MenuItem:
        menu_item = MenuItemMapper.map_serializer_to_domain(serializer_data)        
        return self.menu_repository.create(menu_item)

    def delete_menu_by_id(self, menu_id):
        return self.menu_repository.delete(menu_id)

