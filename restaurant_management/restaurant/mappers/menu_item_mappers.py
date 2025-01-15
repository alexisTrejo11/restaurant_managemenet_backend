from typing import Optional
from datetime import datetime
from decimal import Decimal
from restaurant.services.domain.menu_item import MenuItem, CategoryEnum
from restaurant.models import MenuItemModel

class MenuItemMapper:
     @staticmethod
     def to_domain(model: MenuItemModel) -> MenuItem:
          return MenuItem(
               id=model.id,
               name=model.name,
               price=Decimal(model.price),
               category=model.category,
               description=model.description,
               created_at=model.created_at,
               updated_at=model.updated_at,
          )

     @staticmethod
     def to_model(domain: MenuItem, model: Optional[MenuItemModel] = None) -> MenuItemModel:
        if model is None:
            model = MenuItemModel()
    
            model.id = domain.id
            model.name = domain.name
            model.price = domain.price
            model.description = domain.description
            model.category = domain.category
            model.created_at = domain.created_at
            model.updated_at = domain.updated_at

        return model

     @staticmethod
     def map_serializer_to_domain(serializer) -> MenuItem:
          return MenuItem(
          id=None,
          name=serializer.get('name'),
          price=serializer.get('price'),
          category=CategoryEnum(serializer.get('category')).value,
          description = serializer.get('description')
          )
          

