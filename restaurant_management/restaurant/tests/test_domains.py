import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from restaurant.services.domain.ingredient import Ingredient
from restaurant.services.domain.table import Table


class TestIngredient(unittest.TestCase):
    def setUp(self):
        self.ingredient = Ingredient(
            id="1",
            name="Sugar",
            unit="kg"
        )

    def test_initialization(self):
        self.assertEqual(self.ingredient.id, "1")
        self.assertEqual(self.ingredient.name, "Sugar")
        self.assertEqual(self.ingredient.unit, "kg")
        self.assertIsInstance(self.ingredient.created_at, datetime)
        self.assertIsInstance(self.ingredient.updated_at, datetime)

    def test_update_quantity(self):
        new_quantity = Decimal("10.5")
        initial_updated_at = self.ingredient.updated_at

        self.ingredient.update_quantity(new_quantity)

        self.assertEqual(self.ingredient.quantity, new_quantity)
        self.assertGreater(self.ingredient.updated_at, initial_updated_at)

    def test_update_quantity_negative(self):
        with self.assertRaises(ValueError) as context:
            self.ingredient.update_quantity(Decimal("-5"))
        self.assertEqual(str(context.exception), "Quantity cannot be negative.")

    def test_str_representation(self):
        self.assertEqual(str(self.ingredient), "Sugar")



class TestTable(unittest.TestCase):
    def setUp(self):
        self.table = Table(
            table_number=1,
            capacity=4
        )

    def test_initialization(self):
        self.assertEqual(self.table.table_number, 1)
        self.assertEqual(self.table.capacity, 4)
        self.assertTrue(self.table.is_available)
        self.assertIsInstance(self.table.created_at, datetime)
        self.assertIsInstance(self.table.updated_at, datetime)

    def test_mark_unavailable(self):
        initial_updated_at = self.table.updated_at

        self.table.mark_unavailable()

        self.assertFalse(self.table.is_available)
        self.assertGreater(self.table.updated_at, initial_updated_at)

    def test_mark_available(self):
        self.table.mark_unavailable()
        initial_updated_at = self.table.updated_at

        self.table.mark_available()

        self.assertTrue(self.table.is_available)
        self.assertGreater(self.table.updated_at, initial_updated_at)

    def test_str_representation(self):
        self.assertEqual(str(self.table), "Table 1 (Capacity: 4)")


if __name__ == "__main__":
    unittest.main()
