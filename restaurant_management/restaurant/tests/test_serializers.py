from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from datetime import datetime
from restaurant.serializers import (
    TableInsertSerializer,
    IngredientInsertSerializer,
    MenuInsertItemSerializer,
    StockInsertSerializer,
    ReservationInsertSerializer,
    OrderItemInsertSerializer,
    OrderItemsInsertSerilizer,
    OrderItemsDeleteSerilizer,
    PaymentItemSerializer, 
    PaymentSerializer,
    LoginSerializer, EnumField, UserSerializer, UserInsertSerializer,
    LoginResponseSerializer, PasswordResetSerializer, StaffSignupSerializer
)
from restaurant.serializers import Gender, Role


class TestTableInsertSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "number": 1,
            "capacity": 4
        }
        serializer = TableInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_field(self):
        data = {
            "capacity": 4
        }
        serializer = TableInsertSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("number", serializer.errors)

    def test_invalid_data(self):
        data = {
            "number": "invalid",
            "capacity": "invalid"
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

"""
Reservation Serializers Tests
"""
class TestReservationInsertSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "reservation_date": "2024-12-26T18:00:00Z",
            "customer_number": 4
        }
        serializer = ReservationInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_optional_fields(self):
        data = {
            "name": "John Doe",
            "reservation_date": "2024-12-26T18:00:00Z",
            "customer_number": 4
        }
        serializer = ReservationInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            "name": "John Doe",
            "reservation_date": "invalid",
            "customer_number": "invalid"
        }
        serializer = ReservationInsertSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("reservation_date", serializer.errors)
        self.assertIn("customer_number", serializer.errors)

"""
Order Serializers Tests
"""
class TestOrderItemInsertSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "menu_item_id": 1,
            "quantity": 2,
            "notes": "Extra spicy",
            "menu_extra_id": 10
        }
        serializer = OrderItemInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_optional_fields(self):
        data = {
            "menu_item_id": 1,
            "quantity": 2
        }
        serializer = OrderItemInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_required_field(self):
        data = {
            "quantity": 2
        }
        serializer = OrderItemInsertSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("menu_item_id", serializer.errors)


class TestOrderItemsInsertSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "order_id": 1,
            "order_items": [
                {"menu_item_id": 1, "quantity": 2, "notes": "No onions"},
                {"menu_item_id": 2, "quantity": 1}
            ]
        }
        serializer = OrderItemsInsertSerilizer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_empty_order_items(self):
        data = {
            "order_id": 1,
            "order_items": []
        }
        serializer = OrderItemsInsertSerilizer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("order_items", serializer.errors)


class TestOrderItemsDeleteSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "order_id": 1,
            "item_ids": [1, 2, 3]
        }
        serializer = OrderItemsDeleteSerilizer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_empty_item_ids(self):
        data = {
            "order_id": 1,
            "item_ids": []
        }
        serializer = OrderItemsDeleteSerilizer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("item_ids", serializer.errors)
        
"""
Order Serializers Tests
"""
class TestPaymentItemSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "menu_item_name": "Pizza Margherita",
            "order_item_id": "123",
            "price": "12.50",
            "quantity": 2,
            "total": "25.00",
            "menu_extra_item": "Extra cheese"
        }
        serializer = PaymentItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_optional_field(self):
        data = {
            "menu_item_name": "Pizza Margherita",
            "order_item_id": "123",
            "price": "12.50",
            "quantity": 2,
            "total": "25.00"
        }
        serializer = PaymentItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # `menu_extra_item` es opcional

    def test_missing_required_field(self):
        data = {
            "order_item_id": "123",
            "price": "12.50",
            "quantity": 2
        }
        serializer = PaymentItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("menu_item_name", serializer.errors)


class TestPaymentSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "id": 1,
            "order_id": 123,
            "payment_method": "Credit Card",
            "payment_status": "Completed",
            "sub_total": "50.00",
            "discount": "5.00",
            "vat_rate": "10.00",
            "vat": "4.50",
            "currency_type": "USD",
            "total": "49.50",
            "created_at": "2025-01-14 15:00:00",
            "paid_at": "2025-01-14 15:30:00",
            "items": [
                {
                    "menu_item_name": "Pizza Margherita",
                    "order_item_id": "123",
                    "price": "12.50",
                    "quantity": 2,
                    "total": "25.00"
                },
                {
                    "menu_item_name": "Pasta Carbonara",
                    "order_item_id": "124",
                    "price": "15.00",
                    "quantity": 1,
                    "total": "15.00"
                }
            ]
        }
        serializer = PaymentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_optional_fields(self):
        data = {
            "order_id": 123,
            "payment_method": "Cash",
            "payment_status": "Pending",
            "sub_total": "50.00",
            "discount": "0.00",
            "vat_rate": "10.00",
            "vat": "5.00",
            "currency_type": "USD",
            "total": "55.00",
            "items": [
                {
                    "menu_item_name": "Pizza Margherita",
                    "order_item_id": "123",
                    "price": "12.50",
                    "quantity": 2,
                    "total": "25.00"
                }
            ]
        }
        serializer = PaymentSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # `id`, `created_at` y `paid_at` son opcionales

    def test_empty_items(self):
        data = {
            "order_id": 123,
            "payment_method": "Cash",
            "payment_status": "Pending",
            "sub_total": "50.00",
            "discount": "0.00",
            "vat_rate": "10.00",
            "vat": "5.00",
            "currency_type": "USD",
            "total": "55.00",
            "items": []
        }
        serializer = PaymentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("items", serializer.errors)

    def test_invalid_date_format(self):
        data = {
            "order_id": 123,
            "payment_method": "Cash",
            "payment_status": "Pending",
            "sub_total": "50.00",
            "discount": "0.00",
            "vat_rate": "10.00",
            "vat": "5.00",
            "currency_type": "USD",
            "total": "55.00",
            "created_at": "invalid_date",
            "items": [
                {
                    "menu_item_name": "Pizza Margherita",
                    "order_item_id": "123",
                    "price": "12.50",
                    "quantity": 2,
                    "total": "25.00"
                }
            ]
        }
        serializer = PaymentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("created_at", serializer.errors)


"""
User Auth 
"""

class TestLoginSerializer(APITestCase):
    def test_valid_data(self):
        data = {"identifier_field": "user@example.com", "password": "securepassword"}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_field(self):
        data = {"password": "securepassword"}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("identifier_field", serializer.errors)


class TestUserSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male",
            "email": "john@example.com",
            "password": "securepassword",
            "birth_date": "1990-01-01T00:00:00Z",
            "role": "Admin",
            "joined_at": "2025-01-14T15:00:00Z",
            "last_login": "2025-01-14T15:30:00Z",
            "phone_number": "1234567890"
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_optional_field(self):
        data = {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "gender": "Male",
            "email": "john@example.com",
            "password": "securepassword",
            "birth_date": "1990-01-01T00:00:00Z",
            "role": "Admin",
            "joined_at": "2025-01-14T15:00:00Z",
            "last_login": "2025-01-14T15:30:00Z"
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # `phone_number` es opcional


class TestUserInsertSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": Gender.MALE.value,
            "email": "john@example.com",
            "password": "securepassword",
            "birth_date": "1990-01-01",
            "role": Role.ADMIN.value,
            "phone_number": "1234567890"
        }
        serializer = UserInsertSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_enum(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "InvalidGender",
            "email": "john@example.com",
            "password": "securepassword",
            "birth_date": "1990-01-01",
            "role": Role.ADMIN.value,
            "phone_number": "1234567890"
        }
        serializer = UserInsertSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("gender", serializer.errors)


class TestLoginResponseSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "access_token": "token123",
            "token_type": "Bearer",
            "expires_in": 3600,
            "user": {"id": 1, "first_name": "John"}
        }
        serializer = LoginResponseSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_field(self):
        data = {
            "access_token": "token123",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        serializer = LoginResponseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)


class TestPasswordResetSerializer(APITestCase):
    def test_valid_data(self):
        data = {"email": "user@example.com"}
        serializer = PasswordResetSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        data = {"email": "not-an-email"}
        serializer = PasswordResetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


class TestStaffSignupSerializer(APITestCase):
    def test_valid_data(self):
        data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "gender": Gender.FEMALE.value,
            "email": "alice@example.com",
            "password": "securepassword",
            "birth_date": "1985-05-15",
            "phone_number": "9876543210",
            "role": Role.STAFF.value
        }
        serializer = StaffSignupSerializer(data=data)
        self.assertTrue(serializer.is_valid())
