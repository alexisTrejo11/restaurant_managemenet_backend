from typing import Dict
from ..domain.entities.menu_item import MenuItem
from ..domain.entities.menu_item_extra import MenuExtra
from ...models import MenuExtraModel, MenuItemModel
from ...application.dtos.menu_item_dto import MenuItemDTO
from ...application.dtos.menu_extra_dto import MenuExtraDTO
from decimal import Decimal 

class MenuItemMapper:
    @staticmethod
    def domain_to_dto(menu_item: MenuItem) -> MenuItemDTO:
        return MenuItemDTO(
            id=menu_item.id,
            name=menu_item.name,
            price=str(menu_item.price),
            description=menu_item.description,
            category=menu_item.category,
        )

    @staticmethod
    def dict_to_domain(data: Dict) -> MenuItem:
        """
        Creates a MenuItem domain object from a dictionary.  Useful for
        converting data from a request or other source.
        """
        return MenuItem(
            name=data.get('name'),
            price=Decimal(str(data.get('price'))),
            description=data.get('description'),
            category=data.get('category'),
        )

    @staticmethod
    def domain_to_model(menu_item: MenuItem) -> 'MenuItemModel':
        """
        Creates a MenuItemModel (Django model) instance from a MenuItem domain object.
        """
        if menu_item.id:
            menu_item_model = MenuItemModel.objects.get(pk=menu_item.id)
            menu_item_model.name = menu_item.name
            menu_item_model.price = menu_item.price
            menu_item_model.description = menu_item.description
            menu_item_model.category = menu_item.category
            return menu_item_model
        else:
            return MenuItemModel(
                name=menu_item.name,
                price=menu_item.price,
                description=menu_item.description,
                category=menu_item.category,
            )


    @staticmethod
    def model_to_domain(model: MenuItemModel) -> MenuItem:
        return MenuItem(
            id=model.id,
            name = model.name,
            price = model.price,
            description = model.description,
            category = model.category,
        )
         