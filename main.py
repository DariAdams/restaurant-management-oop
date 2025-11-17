from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.enums import Category, OrderStatus


def main():
    restaurant = Restaurant("Adams Restaurant")

    restaurant.load_data()

    menu = restaurant.menu

    if not menu.list_items():
        margherita = MenuItem(
            name="Margherita Pizza",
            price=45.0,
            category=Category.MainCourse,
            description="Classic pizza with tomatoes, mozzarella, and basil.",
        )

        cheesecake = MenuItem(
            name="Cheesecake",
            price=22.0,
            category=Category.Dessert,
            description="Creamy cheesecake with strawberry sauce.",
        )

        iced_tea = MenuItem(
            name="Iced Tea",
            price=10.0,
            category=Category.Drink,
            description="Cold black tea with lemon.",
        )

        menu.add_item(margherita)
        menu.add_item(cheesecake)
        menu.add_item(iced_tea)

    print("=== RESTAURANT MENU ===")
    print(menu)
    print()

    order = restaurant.create_order() 
    print(f"Created order #{order.order_id} with status: {order.status.value}\n")

    restaurant.add_item_to_order(
        order_id=order.order_id,
        item_name="Margherita Pizza",
        category=Category.MainCourse,
        quantity=2,
    )

    restaurant.add_item_to_order(
        order_id=order.order_id,
        item_name="Iced Tea",
        category=Category.Drink,
        quantity=1,
    )

    print("=== ORDER AFTER ADDING ITEMS ===")
    print(order)
    print()

    restaurant.change_order_item_quantity(
        order_id=order.order_id,
        item_name="Iced Tea",
        category=Category.Drink,
        new_quantity=3,
    )

    print("=== ORDER AFTER CHANGING ICED TEA QUANTITY TO 3 ===")
    print(order)
    print()

    restaurant.remove_item_from_order(
        order_id=order.order_id,
        item_name="Margherita Pizza",
        category=Category.MainCourse,
    )

    print("=== ORDER AFTER REMOVING MARGHERITA ===")
    print(order)
    print()

    restaurant.set_order_status(order_id=order.order_id, new_status=OrderStatus.Completed)

    print("=== FINAL ORDER (COMPLETED) ===")
    print(order)
    print()

    print("=== RESTAURANT OVERVIEW ===")
    print(restaurant)
    print()
    print(f"Total revenue from completed orders: ${restaurant.total_revenue()}")



if __name__ == "__main__":
    main()
