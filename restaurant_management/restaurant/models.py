from django.db import models
from django.utils import timezone

class Ingredient:
    def __init__(self, id, name, unit):
        self.id = id
        self.name = name
        self.unit = unit


class Table():
    def __init__(self, number, seats, is_available):
        self.number = number
        self.seats = seats
        self.is_available = is_available
