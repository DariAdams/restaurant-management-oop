from .enums import Category
from .exceptions import MenuValidationError

class MenuItem:
    def __init__(self, name: str , price: float , category: Category , description: str = "", available: bool = True):
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.available = available

    def update_price(self, new_price: float):
        if new_price <= 0:
            raise MenuValidationError("Price must be strictly greater than 0.")
        self.price = new_price

    def set_availability(self, status: bool):
        if not isinstance(status, bool):
            raise MenuValidationError("Availability status must be a boolean.")
        self.available = status

    def update_description(self, new_description):
        if new_description is None:
            self.description = ""
            return
        if not isinstance(new_description, str):
            raise MenuValidationError("Description must be a string or None.")
        self.description = new_description.strip()

    def to_dict(self):
        item_data = {
            "name": self.name,
            "price": self.price,
            "category": self.category.value,
            "description": self.description,
            "available": self.available
        }
        return item_data

    def __str__(self):
        availability = "Available" if self.available else "Unavailable"
        return f"{self.name} - ${self.price} [{self.category.value}] ({availability})"

    def __repr__(self):
        return (
            f"MenuItem(name={self.name!r}, price={self.price!r}, "
            f"category={self.category!r}, available={self.available!r})"
        )
