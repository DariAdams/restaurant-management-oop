# Restaurant Management App (OOP, Python)

A console-based restaurant management system built using clean Object-Oriented Programming principles in Python.

## Features

### Menu Management
- Add, remove, list, and search menu items
- Categories: Appetizer, Main Course, Dessert, Drink
- Validation for:
  - Name (non-empty)
  - Price (> 0)
  - Availability (boolean)
  - Description (optional string)

### Orders
- `OrderItem` represents a menu item + quantity + subtotal
- `Order` contains multiple items and supports:
  - Add item / change quantity / remove item
  - Calculate total price
  - Status: Pending / Completed / Cancelled

### Restaurant Layer
- `Restaurant` manages:
  - A `Menu`
  - Multiple `Order` objects
- High-level operations:
  - Create orders with auto-incremented IDs
  - Add items to orders using name + category
  - Change quantities and remove items from orders
  - Set order status
  - Calculate total revenue from completed orders

### Persistence
- Menu and orders are saved to JSON:
  - `data/menu.json`
  - `data/orders.json`
- Data is loaded automatically on startup.

## Project Structure

```text
Restaurant-Management-App-OOP/
├── main.py
├── models/
│   ├── menu_item.py
│   ├── menu.py
│   ├── order_item.py
│   ├── order.py
│   ├── restaurant.py
│   ├── enums.py
│   └── exceptions.py
├── utils/
│   ├── json_store.py
│   └── __init__.py
└── data/
    ├── menu.json      # created at runtime
    └── orders.json    # created at runtime
