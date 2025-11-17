from enum import Enum

class Category(Enum):
    Appetizer = "Appetizer"
    MainCourse = "Main Course"
    Dessert = "Dessert"
    Drink = "Drink"


class OrderStatus(Enum):
    Pending = "Pending"
    Completed = "Completed"
    Cancelled = "Cancelled"
