from injector import inject
from typing import Dict, Any, List, Optional
from dataclasses import asdict
from ...core.repositories.menu_item_repository import MenuItemRepository
from ...core.domain.entities.menu_item import MenuItem
from ...core.mappers.menu_item_mapper import MenuItemMapper


class GetMenuByIdUseCase:
    @inject
    def __init__(self, menu_repository: MenuItemRepository):
        self.menu_repository = menu_repository

    def execute(self, menu_id: int,  raise_expection=False) -> Optional[Dict[str, Any]]:
        """
        Retrieve a Menu Item by its ID and return it as a dictionary.
        
        This method performs the following steps:
        1. Fetches the menu item entity from the repository using the provided ID.
        2. Maps the domain entity to a dictionary representation using the MenuItemMapper.
        
        Params:
            - menu_id (int): The ID of the menu item to retrieve.
        
        Returns:
            - Optional[Dict[str, Any]]: A dictionary representation of the menu item.
            - None: If raise expection set as False and entity were not found on repository
        Raises:
            - EntityNotFoundExpection: If raise expection set as True and entity were not found on repository
        
        """
        menu_entity = self.menu_repository.get_by_id(menu_id, raise_expection=raise_expection)
        if not menu_entity:
            return None

        return asdict(MenuItemMapper.to_menu_extra_domain(menu_entity))


class GetAllMenusUseCase:
    @inject
    def __init__(self, menu_repository: MenuItemRepository):
        self.menu_repository = menu_repository

    def execute(self) -> List[Dict[str, Any]]:
        """
        Retrieve all Menu Items and return them as a list of dictionaries.
        
        This method performs the following steps:
        1. Fetches all menu item entities from the repository.
        2. Maps each domain entity to a dictionary representation using the MenuItemMapper.
        
        Params:
            - None
        
        Returns:
            - List[Dict[str, Any]]: A list of dictionary representations of all menu items.
        """
        menu_entity_list = self.menu_repository.get_all()

        return [MenuItemMapper.domain_to_dto(menu_entity) for menu_entity in menu_entity_list]