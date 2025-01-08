from typing import Optional
from restaurant.services.domain.menu_extra import MenuExtraDomain
from restaurant.repository.models.models import MenuExtra

class MenuExtraMapper:
    @staticmethod
    def to_domain(menu_extra_db) -> MenuExtraDomain:
        return MenuExtraDomain(
            name=menu_extra_db.name,
            price=float(menu_extra_db.price),
            description=menu_extra_db.description,
            created_at=menu_extra_db.created_at,
            updated_at=menu_extra_db.updated_at
        )

    @staticmethod
    def to_model(menu_extra_domain: MenuExtraDomain) -> MenuExtra :
        return MenuExtra(
            name=menu_extra_domain.name,
            price=menu_extra_domain.price,
            description=menu_extra_domain.description,
            created_at=menu_extra_domain.created_at,
            updated_at=menu_extra_domain.updated_at
        )
