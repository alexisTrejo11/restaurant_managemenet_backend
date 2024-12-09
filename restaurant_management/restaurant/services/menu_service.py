from restaurant.models import MenuItem
from restaurant.serializers import MenuSerializer
from rest_framework.exceptions import ValidationError


class MenuService:
    @staticmethod
    def get_menu_by_id(menu_id):
        try:
            menu = MenuItem.objects.get(id=menu_id)
            return MenuSerializer(menu).data
        except Menu.DoesNotExist:
            return None


    @staticmethod
    def get_menus_by_category(category):
        try:
            Menus = MenuItem.objects.filter(category=category)
            serialier = MenuSerializer(Menus, many=True)
            serialier.data
        except Menu.DoesNotExist:
            return None

    @staticmethod
    def create_menu(data):
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError(serializer.errors)


    @staticmethod
    def delete_menu_by_id(menu_id):
        try:
            menu = MenuItem.objects.get(id=menu_id)
            menu.delete()
            return True
        except Menu.DoesNotExist:
            return False

