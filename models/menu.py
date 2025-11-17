from .menu_item import MenuItem
from .enums import Category
from .exceptions import MenuItemExistsError ,MenuItemNotFoundError

class Menu:
  def __init__(self):
    self._items = {}
  
  def _normalize_name(self, name: str) -> str:
    return name.strip().lower()
  
  def _make_key(self, name: str, category: Category):
    normalized = self._normalize_name(name)
    return (normalized, category)
  
  def add_item(self, item: MenuItem):
    key = self._make_key(item.name, item.category)
    if key in self._items:
        raise MenuItemExistsError("Item already exists in menu.")
    self._items[key] = item

  def remove_item(self, name: str, category: Category):
    key = self._make_key(name, category)
    if key not in self._items:
      raise MenuItemNotFoundError("Item not found in menu.")
    del self._items[key]

  def get_item(self, name: str, category: Category):
    key = self._make_key(name, category)
    if key in self._items:
      return self._items[key]
    return None
  
  def list_items(self, category: Category = None):
    if category is None:
     return list(self._items.values())
     
    filtered_items = []

    for item in self._items.values():
       if item.category == category:
         filtered_items.append(item)
    return  filtered_items
  
  def update_item_price(self, name, category, new_price):
    key = self._make_key(name, category)

    if key not in self._items:
      raise MenuItemNotFoundError("Item not found in menu.")
    item = self._items[key]
    item.update_price(new_price)

  def set_item_availability(self, name, category, status):
    key = self._make_key(name, category)

    if key not in self._items:
      raise MenuItemNotFoundError("Item not found in menu.")
    item = self._items[key]
    item.set_availability(status)

  def search(self, keyword: str):
    normalized = keyword.strip().lower()
    results = []
    
    for item in self._items.values():
      name_match = normalized in item.name.lower()
      description_match = normalized in item.description.lower()
      if name_match or description_match:
        results.append(item)
    return results
  
  def __str__(self):
    if not self._items:
        return "Menu is empty."
    
    lines = []

    categories = {}
    for item in self._items.values():
        categories.setdefault(item.category, []).append(item)
    
    for category in sorted(categories.keys(), key=lambda c: c.value):
        lines.append(f"=== {category.value} ===")
        for item in categories[category]:
            lines.append(str(item))
        lines.append("") 

    return "\n".join(lines).strip()

  