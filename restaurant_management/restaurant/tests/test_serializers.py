from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from restaurant.serializers import (
    TableInsertSerializer,
    IngredientInsertSerializer,
    MenuInsertItemSerializer,
    StockInsertSerializer,
    ReservationInsertSerializer,
)

class TestTableInsertSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "number": 1,
            "seats": 4
        }
        serializer = TableInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_field(self):
        data = {
            "seats": 4
        }
        serializer = TableInsertSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("number", serializer.errors)

    def test_invalid_data(self):
        data = {
            "number": "invalid",
            "seats": "invalid"
        }
        serializer = TableInsertSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class TestIngredientInsertSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "name": "Salt",
            "quantity": 10,
            "unit": "kg"
        }
        serializer = IngredientInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_field(self):
        data = {
            "name": "Salt",
        }
        serializer = IngredientInsertSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("unit", serializer.errors)

class TestMenuInsertItemSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "name": "Burger",
            "price": "12.99",
            "category": "MEALS",
            "description": "Delicious burger"
        }
        serializer = MenuInsertItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_category(self):
        data = {
            "name": "Burger",
            "price": "12.99",
            "category": "UNKNOWN",
            "description": "Delicious burger"
        }
        serializer = MenuInsertItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)

class TestStockInsertSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "ingredient_id": 1,
            "optimal_stock_quantity": 100
        }
        serializer = StockInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_field(self):
        data = {
            "optimal_stock_quantity": 100
        }
        serializer = StockInsertSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("ingredient_id", serializer.errors)

class TestReservationInsertSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "requested_reservation_time": "2024-12-26T18:00:00Z",
            "customer_number": 4
        }
        serializer = ReservationInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_optional_fields(self):
        data = {
            "name": "John Doe",
            "requested_reservation_time": "2024-12-26T18:00:00Z",
            "customer_number": 4
        }
        serializer = ReservationInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            "name": "John Doe",
            "requested_reservation_time": "invalid",
            "customer_number": "invalid"
        }
        serializer = ReservationInsertSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("requested_reservation_time", serializer.errors)
        self.assertIn("customer_number", serializer.errors)
