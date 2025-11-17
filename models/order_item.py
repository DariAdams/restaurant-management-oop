from .menu_item import MenuItem
from .exceptions import MenuValidationError

class OrderItem:
   def __init__(self, item: MenuItem, quantity: int):
    if not isinstance(item, MenuItem):
      raise MenuValidationError("Item must be a MenuItem instance.")
    
    if not isinstance(quantity, int):
      raise MenuValidationError("Quantity must be an integer.")
    
    if quantity < 1:
      raise MenuValidationError("Quantity must be at least 1.")
    
    self.item = item
    self.quantity = quantity
   
   def update_quantity(self, new_quantity):
    if not isinstance(new_quantity, int):
      raise MenuValidationError("Quantity must be an integer.")
    
    if new_quantity < 1:
      raise MenuValidationError("Quantity must be at least 1.")
    
    self.quantity = new_quantity
    
   def subtotal(self):
     return self.item.price * self.quantity
   
   def to_dict(self):
    return {
        "item": self.item.to_dict(),
        "quantity": self.quantity,
        "subtotal": self.subtotal(),
    }
   
   def __str__(self):
    return f"{self.quantity} x {self.item.name} -> ${self.subtotal()}"
   
   def __repr__(self):
    return (
        f"OrderItem(item={self.item!r}, "
        f"quantity={self.quantity!r})"
    )
