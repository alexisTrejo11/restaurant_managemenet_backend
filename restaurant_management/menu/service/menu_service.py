from ..repository.menu_item_repository import MenuItemRepository
from common.mappers.menu_item_mappers import MenuItemMapper
from restaurant.services.domain.menu_item import MenuItem
from injector import inject
from django.core.cache import cache 
import logging

logger = logging.getLogger(__name__)

class MenuItemService:
    @inject
    def __init__(self, menu_repository: MenuItemRepository):
        self.menu_repository = menu_repository
    
    def get_menu_by_id(self, menu_id) -> MenuItem:
        menu = cache.get(f'menu_{menu_id}')

        if menu is None:
            menu = self.menu_repository.get_by_id(menu_id)
            cache.set(f'menu_{menu_id}', menu, timeout=36000)
        
        return menu

    def get_all_menus(self) -> list:
        menus = cache.get('all_menus')

        if menus is None:
            menus = self.menu_repository.get_all()
            cache.set('all_menus', menus, timeout=36000)

        return menus

    def create_menu(self, serializer_data) -> MenuItem:
        menu_item = MenuItemMapper.map_serializer_to_domain(serializer_data)
        
        created_menu = self.menu_repository.create(menu_item)
        
        logger.info(f"Menu with ID {created_menu.id} created successfully.")
        return created_menu

    def delete_menu_by_id(self, menu_id):
        is_delete = self.menu_repository.delete(menu_id)
        
        if is_delete:
            logger.info(f"Menu with ID {menu_id} deleted successfully.")
        return is_delete

