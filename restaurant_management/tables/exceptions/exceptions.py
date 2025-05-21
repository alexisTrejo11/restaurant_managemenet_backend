# your_app_name/exceptions/exceptions.py
from rest_framework.exceptions import APIException
from rest_framework import status

class TableCapacityExceeded(APIException):
    """
    Exception raised when the provided table capacity exceeds the maximum allowed.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Table capacity is out of range."
    default_code = "table_capacity_exceeded"

class RestaurantCapacityFull(APIException):
    """
    Exception raised when trying to create a new table but the restaurant
    has already reached its maximum allowed number of tables.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Restaurant is at maximum table capacity."
    default_code = "restaurant_capacity_full"

class TableNumberAlreadyExists(APIException):
    """
    Exception raised when attempting to create or update a table with a number
    that is already assigned to another table.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Table number already exists."
    default_code = "table_number_already_exists"

class TableInUse(APIException):
    """
    Exception raised when attempting to delete a table that is currently in use
    (e.g., has active reservations).
    """
    status_code = status.HTTP_409_CONFLICT # Conflict with current state
    default_detail = "Cannot delete table as it is currently in use or has active dependencies."
    default_code = "table_in_use"