from typing import Dict
from ..domain.entities.menu_item import MenuItem
from ..domain.entities.menu_item_extra import MenuExtra
from ...models import MenuExtraModel, MenuItemModel
from ...application.dtos.menu_extra_dto import MenuExtraDTO
from decimal import Decimal 

class MenuExtraMapper:
    @staticmethod
    def domain_to_dto(menu_extra: MenuExtra) -> MenuExtraDTO:
        return MenuExtraDTO(
            id=menu_extra.id,
            name=menu_extra.name,
            price=str(menu_extra.price),
            description=menu_extra.description,
        )

    @staticmethod
    def dict_to_domain(data: Dict) -> MenuExtra:
        """
        Creates a MenuExtra domain object from a dictionary.
        """
        return MenuExtra(
            name=data.get('name'),
            price=Decimal(str(data.get('price'))),
            description=data.get('description'),
        )

    @staticmethod
    def domain_to_model(menu_extra: MenuExtra) -> MenuExtraModel:
        """
        Creates a MenuExtraModel (Django model) instance from a MenuExtra domain object.
        """
        if menu_extra.id:
            menu_extra_model = MenuExtraModel.objects.get(pk=menu_extra.id)
            menu_extra_model.name = menu_extra.name
            menu_extra_model.price = menu_extra.price
            menu_extra_model.description = menu_extra.description
            return menu_extra_model
        else:
            return MenuExtraModel(
                name=menu_extra.name,
                price=menu_extra.price,
                description=menu_extra.description,
            )