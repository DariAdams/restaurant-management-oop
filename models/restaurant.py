from .menu import Menu
from .order import Order
from .menu_item import MenuItem
from .enums import Category, OrderStatus
from .exceptions import MenuItemNotFoundError, MenuValidationError
from utils.json_store import save_json, load_json


class Restaurant:
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise MenuValidationError("Restaurant name must be a non-empty string.")

        self.name = name.strip()
        self.menu = Menu()
        self._orders: dict[int, Order] = {}
        self._next_order_id: int = 1


    def create_order(self) -> Order:
        """
        Create a new order with an auto-incremented ID and status Pending.
        Returns the created Order instance.
        """
        order = Order(order_id=self._next_order_id, status=OrderStatus.Pending)
        self._orders[order.order_id] = order
        self._next_order_id += 1
        return order

    def get_order(self, order_id: int) -> Order | None:
        """
        Return an Order by ID, or None if it doesn't exist.
        """
        return self._orders.get(order_id)

    def require_order(self, order_id: int) -> Order:
        """
        Internal helper: returns the Order or raises MenuValidationError if not found.
        """
        order = self.get_order(order_id)
        if order is None:
            raise MenuValidationError(f"Order with ID {order_id} does not exist.")
        return order

    def list_orders(self) -> list[Order]:
        """
        Return a list of all orders in the restaurant.
        """
        return list(self._orders.values())

    def list_orders_by_status(self, status: OrderStatus) -> list[Order]:
        """
        Return a list of orders filtered by their status.
        """
        if not isinstance(status, OrderStatus):
            raise MenuValidationError("status must be an OrderStatus value.")
        return [order for order in self._orders.values() if order.status == status]

    def _get_menu_item_or_raise(self, name: str, category: Category) -> MenuItem:
        """
        Helper: fetch item from menu or raise MenuItemNotFoundError.
        """
        item = self.menu.get_item(name, category)
        if item is None:
            raise MenuItemNotFoundError("Item not found in menu.")
        return item

    def add_item_to_order(
        self,
        order_id: int,
        item_name: str,
        category: Category,
        quantity: int = 1,
    ) -> None:
        """
        Add a menu item to an existing order by order_id.
        If the item already exists in the order, increases its quantity.
        """
        order = self.require_order(order_id)
        menu_item = self._get_menu_item_or_raise(item_name, category)
        order.add_item(menu_item, quantity)

    def change_order_item_quantity(
        self,
        order_id: int,
        item_name: str,
        category: Category,
        new_quantity: int,
    ) -> None:
        """
        Change the quantity of an item inside a given order.
        """
        order = self.require_order(order_id)
        menu_item = self._get_menu_item_or_raise(item_name, category)
        order.change_item_quantity(menu_item, new_quantity)

    def remove_item_from_order(
        self,
        order_id: int,
        item_name: str,
        category: Category,
    ) -> None:
        """
        Remove an item completely from an order.
        """
        order = self.require_order(order_id)
        menu_item = self._get_menu_item_or_raise(item_name, category)
        order.remove_item(menu_item)


    def set_order_status(self, order_id: int, new_status: OrderStatus) -> None:
        """
        Update the status of an order (Pending / Completed / Cancelled).
        """
        order = self.require_order(order_id)
        order.set_status(new_status)


    def total_revenue(self) -> float:
        """
        Sum of totals for all completed orders.
        """
        return sum(
            order.total()
            for order in self._orders.values()
            if order.status == OrderStatus.Completed
        )

    def to_dict(self) -> dict:
        """
        Serialize the restaurant, including menu and all orders.
        """
        return {
            "name": self.name,
            "menu": [item.to_dict() for item in self.menu.list_items()],
            "orders": [order.to_dict() for order in self.list_orders()],
            "total_revenue": self.total_revenue(),
        }


    def save_data(self, menu_file: str = "data/menu.json", orders_file: str = "data/orders.json") -> None:
        """
        Save menu and orders to JSON files.
        """

        menu_data = [item.to_dict() for item in self.menu.list_items()]
        save_json(menu_data, menu_file)

        orders_data = [order.to_dict() for order in self.list_orders()]
        save_json(orders_data, orders_file)

    def load_data(self, menu_file: str = "data/menu.json", orders_file: str = "data/orders.json") -> None:
        """
        Load menu and orders from JSON files, if they exist.
        """
        from .order_item import OrderItem 

        menu_data = load_json(menu_file)
        if menu_data:
            for item_data in menu_data:
                item = MenuItem(
                    name=item_data["name"],
                    price=item_data["price"],
                    category=Category(item_data["category"]),
                    description=item_data["description"],
                    available=item_data["available"],
                )

                if self.menu.get_item(item.name, item.category) is None:
                    self.menu.add_item(item)

        orders_data = load_json(orders_file)
        max_order_id = 0

        if orders_data:
            for od in orders_data:
                order = Order(
                    order_id=od["order_id"],
                    status=OrderStatus(od["status"])
                )
                self._orders[order.order_id] = order
                max_order_id = max(max_order_id, order.order_id)

                for item_dict in od["items"]:
                    item_data = item_dict["item"]
                    category = Category(item_data["category"])

                    menu_item = self.menu.get_item(item_data["name"], category)
                    if menu_item is None:
                        menu_item = MenuItem(
                            name=item_data["name"],
                            price=item_data["price"],
                            category=category,
                            description=item_data["description"],
                            available=item_data["available"],
                        )
                        self.menu.add_item(menu_item)

                    order.add_item(menu_item, item_dict["quantity"])

        if max_order_id > 0:
            self._next_order_id = max_order_id + 1
        else:
            self._next_order_id = 1

    def __str__(self) -> str:
        lines = [f"Restaurant: {self.name}", ""]

        lines.append("=== MENU ===")
        lines.append(str(self.menu))
        lines.append("")

        if not self._orders:
            lines.append("No orders yet.")
        else:
            lines.append("=== ORDERS ===")
            for order in self.list_orders():
                lines.append(str(order))
                lines.append("")

        return "\n".join(lines).strip()

    def __repr__(self) -> str:
        return (
            f"Restaurant(name={self.name!r}, "
            f"orders={len(self._orders)!r})"
        )
