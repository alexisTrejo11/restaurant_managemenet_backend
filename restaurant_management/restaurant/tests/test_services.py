import pytest
from mockito import mock, verify, when, any, eq
from orders.services.table_service import TableService
from restaurant.repository.table_respository import TableRepository
from restaurant_management.reservations.domain.entities.table import Table

@pytest.fixture
def table_repository_mock():
    return mock(TableRepository)

@pytest.fixture
def table_service(table_repository_mock):
    return TableService(table_repository=table_repository_mock)

def test_get_table_by_number(table_service, table_repository_mock):
    # Arrange
    mock_table = Table(number=1, capacity=4, is_available=True)
    when(table_repository_mock).get_by_id(1).thenReturn(mock_table)

    # Act
    result = table_service.get_table_by_number(1)

    # Asser
    assert result == mock_table
    verify(table_repository_mock).get_by_id(1) 

def test_get_all_tables(table_service, table_repository_mock):
    # Arrange
    mock_tables = [Table(number=1, capacity=4, is_available=True), Table(number=2, capacity=2, is_available=True)]
    when(table_repository_mock).get_all().thenReturn(mock_tables)

    # Act
    result = table_service.get_all_tables()

    # Asser
    assert result == mock_tables
    verify(table_repository_mock).get_all()  

def test_validate_unique_table_number(table_service, table_repository_mock):
    # Arrange
    when(table_repository_mock).get_by_id(number=1).thenReturn(None) 
    
    # Act
    result = table_service.validate_unique_table_number({'number': 1, 'capacity': 4})

    # Asser
    assert result is True
    verify(table_repository_mock).get_by_id(number=1)

def test_create_table(table_service, table_repository_mock):
    # Arrange
    new_table = Table(number=1, capacity=4, is_available=True)
    when(table_repository_mock).create(any).thenReturn(new_table)

    # Act
    result = table_service.create_table({'number': 1, 'capacity': 4})

    # Asser
    assert result == new_table
    verify(table_repository_mock).create(any)

def test_delete_table(table_service, table_repository_mock):
    # Arrange
    when(table_repository_mock).delete(1).thenReturn(True)

    # Act
    result = table_service.delete_table(1)

    # Asser
    assert result is True
    verify(table_repository_mock).delete(1)


import pytest
from mockito import mock, verify, when
from restaurant.services.menu_service import MenuItemService
from restaurant.repository.menu_item_repository import MenuItemRepository
from restaurant.services.domain.menu_item import MenuItem
from django.core.cache import cache
 
@pytest.fixture
def menu_repository_mock():
    return mock(MenuItemRepository)

@pytest.fixture
def menu_service(menu_repository_mock):
    return MenuItemService(menu_repository=menu_repository_mock)

def test_get_menu_by_id_from_cache(menu_service, menu_repository_mock):
    # Arrange
    menu_id = 1
    mock_menu = MenuItem(id=menu_id, name="Pizza", description="Delicious pizza", price=10.99, category="MEALS")
    cache.set(f'menu_{menu_id}', mock_menu)

    # Act
    result = menu_service.get_menu_by_id(menu_id)

    # Asser
    assert result.id == mock_menu.id
    assert result.name == mock_menu.name
    assert result.description == mock_menu.description
    assert result.price == mock_menu.price
    assert result.category == mock_menu.category

def test_get_menu_by_id_from_repository(menu_service, menu_repository_mock):
    # Arrange
    menu_id = 1
    mock_menu = MenuItem(id=menu_id, name="Pizza", description="Delicious pizza", price=10.99, category="MEALS")
    when(menu_repository_mock).get_by_id(menu_id).thenReturn(mock_menu)

    # Act
    result = menu_service.get_menu_by_id(menu_id)

    # Asser
    assert result.id == mock_menu.id
    assert result.name == mock_menu.name
    assert result.description == mock_menu.description
    assert result.price == mock_menu.price
    assert result.category == mock_menu.category

def test_get_all_menus_from_cache(menu_service, menu_repository_mock):
    # Arrange
    mock_menus = [
        MenuItem(id=1, name="Pizza", description="Delicious pizza", price=10.99, category="MEALS"),
        MenuItem(id=2, name="Burger", description="Tasty burger", price=8.99, category="MEALS")
    ]
    cache.set('all_menus', mock_menus)

    # Act
    result = menu_service.get_all_menus()

    # Asser
    assert len(result) == len(mock_menus)
    for i, menu in enumerate(result):
        assert menu.id == mock_menus[i].id
        assert menu.name == mock_menus[i].name
        assert menu.description == mock_menus[i].description
        assert menu.price == mock_menus[i].price
        assert menu.category == mock_menus[i].category

def test_get_all_menus_from_repository(menu_service, menu_repository_mock):
    # Arrange
    mock_menus = [
        MenuItem(id=1, name="Pizza", description="Delicious pizza", price=10.99, category="MEALS"),
        MenuItem(id=2, name="Burger", description="Tasty burger", price=8.99, category="MEALS")
    ]
    when(menu_repository_mock).get_all().thenReturn(mock_menus)

    # Act
    result = menu_service.get_all_menus()

    # Asser
    assert len(result) == len(mock_menus)
    for i, menu in enumerate(result):
        assert menu.id == mock_menus[i].id
        assert menu.name == mock_menus[i].name
        assert menu.description == mock_menus[i].description
        assert menu.price == mock_menus[i].price
        assert menu.category == mock_menus[i].category

def test_create_menu(menu_service, menu_repository_mock):
    # Arrange
    serializer_data = {'name': 'Pizza', 'description': 'Delicious pizza', 'price': 10.99, 'category': 'MEALS'}
    mock_menu = MenuItem(id=1, name="Pizza", description="Delicious pizza", price=10.99, category="MEALS")
    
    # Crear un stub con un objeto similar, pero utilizando los valores
    when(menu_repository_mock).create(any()).thenReturn(mock_menu)

    # Act
    result = menu_service.create_menu(serializer_data)

    # Asser
    assert result.id == mock_menu.id
    assert result.name == mock_menu.name
    assert result.description == mock_menu.description
    assert result.price == mock_menu.price
    assert result.category == mock_menu.category
    
    verify(menu_repository_mock).create(any())

def test_delete_menu_by_id(menu_service, menu_repository_mock):
    # Arrange
    menu_id = 1
    when(menu_repository_mock).delete(menu_id).thenReturn(True)

    # Act
    result = menu_service.delete_menu_by_id(menu_id)

    # Asser
    assert result is True  # El menú debe ser eliminado correctamente
    verify(menu_repository_mock).delete(menu_id)  # El repositorio debe ser llamado para eliminar el menú

import pytest
from unittest.mock import MagicMock, patch
from restaurant.services.ingredient_service import IngredientService
from restaurant.services.domain.ingredient import Ingredient
from django.core.cache import cache

@pytest.fixture
def ingredient_service():
    # Arrange
    ingredient_repository_mock = MagicMock()
    return IngredientService(ingredient_repository=ingredient_repository_mock), ingredient_repository_mock

def test_get_ingredient_by_id_from_cache(ingredient_service):
    # Arrange
    ingredient_service, _ = ingredient_service
    ingredient_id = 1
    mock_ingredient = Ingredient(id=ingredient_id, name="Tomato", unit="kg")
    cache.set(f'ingredient_{ingredient_id}', mock_ingredient)  
    
    # Act
    result = ingredient_service.get_ingredient_by_id(ingredient_id)
    
    # Assert
    assert result.id == mock_ingredient.id
    assert result.name == mock_ingredient.name
    assert result.unit == mock_ingredient.unit

@patch('django.core.cache.cache.set')
def test_get_ingredient_by_id_from_repository(mock_cache_set, ingredient_service):
    # Arrange
    ingredient_service, ingredient_repository_mock = ingredient_service
    ingredient_id = 1
    mock_ingredient = Ingredient(id=ingredient_id, name="Tomato", unit="kg")
    cache.delete(f'ingredient_{ingredient_id}')  
    ingredient_repository_mock.get_by_id.return_value = mock_ingredient 

    # Act
    result = ingredient_service.get_ingredient_by_id(ingredient_id)
    
    # Assert
    assert result.id == mock_ingredient.id
    assert result.name == mock_ingredient.name
    assert result.unit == mock_ingredient.unit
    ingredient_repository_mock.get_by_id.assert_called_once() 
    mock_cache_set.assert_called_once_with(f'ingredient_{ingredient_id}', mock_ingredient, timeout=3600)

def test_get_all_ingredients_from_cache(ingredient_service):
    # Arrange
    ingredient_service, _ = ingredient_service
    mock_ingredients = [
        Ingredient(id=1, name="Tomato", unit="kg"),
        Ingredient(id=2, name="Onion", unit="kg")
    ]
    cache.set('all_ingredients', mock_ingredients)
    
    # Act
    result = ingredient_service.get_all_ingredients()
    
    # Assert
    assert len(result) == len(mock_ingredients) 
    for res, mock in zip(result, mock_ingredients):
        assert res.id == mock.id
        assert res.name == mock.name
        assert res.unit == mock.unit

@patch('django.core.cache.cache.set')
def test_get_all_ingredients_from_repository(mock_cache_set, ingredient_service):
    # Arrange
    ingredient_service, ingredient_repository_mock = ingredient_service
    mock_ingredients = [
        Ingredient(id=1, name="Tomato", unit="kg"),
        Ingredient(id=2, name="Onion", unit="kg")
    ]
    ingredient_repository_mock.get_all.return_value = mock_ingredients
    cache.delete('all_ingredients')  
    
    # Act
    result = ingredient_service.get_all_ingredients()
    
    # Assert
    assert len(result) == len(mock_ingredients) 
    for res, mock in zip(result, mock_ingredients):
        assert res.id == mock.id
        assert res.name == mock.name
        assert res.unit == mock.unit
    ingredient_repository_mock.get_all.assert_called_once() 
    mock_cache_set.assert_called_once_with('all_ingredients', mock_ingredients, timeout=600) 

def test_create_ingredient(ingredient_service):
    # Arrange
    ingredient_service, ingredient_repository_mock = ingredient_service
    ingredient_data = {'name': 'Tomato', 'unit': 'kg'}
    mock_ingredient = Ingredient(id=1, name="Tomato", unit="kg")  
    ingredient_repository_mock.create.return_value = mock_ingredient
    
    # Act
    result = ingredient_service.create_ingredient(ingredient_data)
    
    # Assert
    assert result.id == mock_ingredient.id
    assert result.name == mock_ingredient.name
    assert result.unit == mock_ingredient.unit
