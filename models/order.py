from .order_item import OrderItem
from .menu_item import MenuItem
from .enums import Category, OrderStatus
from .exceptions import MenuValidationError, MenuItemNotFoundError


class Order:
    def __init__(self, order_id: int, status: OrderStatus = OrderStatus.Pending):
        if not isinstance(order_id, int):
            raise MenuValidationError("order_id must be an integer.")

        if order_id < 1:
            raise MenuValidationError("order_id must be at least 1.")

        if not isinstance(status, OrderStatus):
            raise MenuValidationError("status must be an OrderStatus value.")

        self.order_id = order_id
        self.status = status
        self._items: dict[tuple[str, Category], OrderItem] = {}


    def _normalize_name(self, name: str) -> str:
        return name.strip().lower()

    def _make_key(self, name: str, category: Category) -> tuple[str, Category]:
        normalized = self._normalize_name(name)
        return (normalized, category)

    def _make_key_from_item(self, item: MenuItem) -> tuple[str, Category]:
        return self._make_key(item.name, item.category)

    def add_item(self, item: MenuItem, quantity: int = 1) -> None:
        """
        Add a menu item to this order.
        If the item already exists in the order, increase its quantity.
        """
        if not isinstance(item, MenuItem):
            raise MenuValidationError("item must be a MenuItem instance.")

        if not isinstance(quantity, int):
            raise MenuValidationError("quantity must be an integer.")

        if quantity < 1:
            raise MenuValidationError("quantity must be at least 1.")

        key = self._make_key_from_item(item)

        if key in self._items:
            existing_order_item = self._items[key]
            new_quantity = existing_order_item.quantity + quantity
            existing_order_item.update_quantity(new_quantity)
        else:
            self._items[key] = OrderItem(item=item, quantity=quantity)

    def change_item_quantity(self, item: MenuItem, new_quantity: int) -> None:
        """
        Set a new quantity for an item in the order.
        """
        if not isinstance(new_quantity, int):
            raise MenuValidationError("new_quantity must be an integer.")

        if new_quantity < 1:
            raise MenuValidationError("new_quantity must be at least 1.")

        key = self._make_key_from_item(item)

        if key not in self._items:
            raise MenuItemNotFoundError("Item not found in this order.")

        order_item = self._items[key]
        order_item.update_quantity(new_quantity)

    def remove_item(self, item: MenuItem) -> None:
        """
        Remove an item completely from the order.
        """
        key = self._make_key_from_item(item)

        if key not in self._items:
            raise MenuItemNotFoundError("Item not found in this order.")

        del self._items[key]


    def get_items(self) -> list[OrderItem]:
        """
        Return a list of OrderItem objects in this order.
        """
        return list(self._items.values())

    def total(self) -> float:
        """
        Calculate the total cost of the order.
        """
        return sum(order_item.subtotal() for order_item in self._items.values())


    def set_status(self, new_status: OrderStatus) -> None:
        if not isinstance(new_status, OrderStatus):
            raise MenuValidationError("new_status must be an OrderStatus value.")
        self.status = new_status

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "status": self.status.value,
            "items": [oi.to_dict() for oi in self.get_items()],
            "total": self.total(),
        }

    def __str__(self) -> str:
        if not self._items:
            return f"Order #{self.order_id} ({self.status.value}) - empty"

        lines = [f"Order #{self.order_id} ({self.status.value})"]

        for order_item in self.get_items():
            lines.append(str(order_item))

        lines.append(f"Total: ${self.total()}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"Order(order_id={self.order_id!r}, "
            f"status={self.status!r}, "
            f"items={self.get_items()!r})"
        )
