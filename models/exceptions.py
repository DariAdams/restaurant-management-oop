class MenuValidationError(Exception):
    """Raised when a menu item has invalid data, like empty name or negative price."""
    pass

class MenuItemExistsError(Exception):
    """Raised when trying to add a duplicate item to the menu."""
    pass

class MenuItemNotFoundError(Exception):
    """Raised when a menu item is not found."""
    pass
