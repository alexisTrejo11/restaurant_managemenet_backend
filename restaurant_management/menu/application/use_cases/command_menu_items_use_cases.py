from injector import inject
from typing import Dict, Any
from ...core.repositories.menu_item_repository import MenuItemRepository
from ...core.domain.entities.menu_item import MenuItem
from ...core.mappers.menu_item_mapper import MenuItemMapper
from ..dtos.menu_item_dto import MenuItemDTO

class CreateMenuUseCase:
    @inject
    def __init__(self, menu_repository: MenuItemRepository):
        self.menu_repository = menu_repository

    def execute(self, serializer_data: Dict) -> MenuItem:
        """
        Create a new Menu Item from the provided serialized data.
        
        This method performs the following steps:
        1. Maps the serialized data to a domain entity using the MenuItemMapper.
        2. Validates the created domain entity.
        3. Persists the validated entity in the repository.
        
        Params:
            - serializer_data (Dict): A dictionary containing the serialized data for the menu item.
        
        Returns:
            - MenuItem: The newly created menu item as a DTO data class.
        """
        menu_item = MenuItemMapper.dict_to_domain(serializer_data)

        menu_item.validate()

        created_menu = self.menu_repository.save(menu_item)

        return MenuItemMapper.domain_to_dto(created_menu)


class DeleteMenuUseCase:
    @inject
    def __init__(self, menu_repository: MenuItemRepository):
        self.menu_repository = menu_repository

    def execute(self, menu_id: int) -> None:
        """
        Delete A Menu Item By His ID. Will raise an exception if entity is not founded.
        
        Params:
            - menu_id (int): The ID of the menu item to delete.
        
        Returns:
            - None
        """
        self.menu_repository.get_by_id(menu_id, raise_expection=True)

        self.menu_repository.delete(menu_id)