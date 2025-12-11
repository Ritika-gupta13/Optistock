import json
import os
from datetime import datetime
from typing import List, Optional, Dict
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# --- File Constants ---
INVENTORY_FILE = 'inventory_data.json'
TRANSACTIONS_FILE = 'transactions_data.json'
USERS_FILE = 'users_data.json'

# --- Product Management Classes ---

class Product:
    def __init__(self, item_code, name, price, stock):
        self.item_code = item_code
        self.name = name
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            'item_code': self.item_code,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }

# --- User Management Classes (CLEANED) ---

class User(UserMixin):
    """Represents a user in the system for local login."""
    def __init__(self, user_id, username, password_hash=None):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        # google_id and email removed

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            # google_id and email removed
        }

# --- Inventory I/O ---

def load_inventory() -> List[Product]:
    if not os.path.exists(INVENTORY_FILE):
        return []
    try:
        with open(INVENTORY_FILE, 'r') as f:
            data = json.load(f)
            return [Product(**item) for item in data]
    except (IOError, json.JSONDecodeError):
        return []

def save_inventory(inventory: List[Product]):
    data = [p.to_dict() for p in inventory]
    try:
        with open(INVENTORY_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        print("Error: Could not save inventory file.")

def find_product(inventory: List[Product], item_code: str) -> Optional[Product]:
    return next((p for p in inventory if p.item_code == item_code), None)

def get_total_inventory_value(inventory: List[Product]) -> float:
    return sum(p.price * p.stock for p in inventory)

def get_low_stock_items(inventory: List[Product], threshold: int = 10) -> List[Product]:
    return [p for p in inventory if p.stock <= threshold]

# --- Transaction I/O and Reporting ---

def load_transactions() -> list:
    if not os.path.exists(TRANSACTIONS_FILE):
        return []
    try:
        with open(TRANSACTIONS_FILE, 'r') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return []

def save_transaction(transaction: Dict):
    transactions = load_transactions()
    transactions.append(transaction)
    try:
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump(transactions, f, indent=4)
    except IOError:
        print("Error: Could not save transactions file.")

def record_sale(inventory: List[Product], item_code: str, quantity: int) -> Optional[Dict]:
    product = find_product(inventory, item_code.upper())
    
    if product and quantity > 0 and product.stock >= quantity:
        product.stock -= quantity
        revenue = quantity * product.price
        
        transaction = {
            'timestamp': datetime.now().isoformat(),
            'item_code': product.item_code,
            'name': product.name,
            'quantity': quantity,
            'price_at_sale': product.price,
            'revenue': revenue
        }
        save_transaction(transaction)
        return transaction
    return None

def get_best_selling_items(transactions: list, top_n: int = 5) -> List[Dict]:
    """Calculates total quantity sold for each item and returns the top N."""
    sales_summary = {}
    
    for t in transactions:
        code = t['item_code']
        quantity = t['quantity']
        
        if code not in sales_summary:
            sales_summary[code] = {
                'item_code': code,
                'name': t['name'],
                'total_quantity_sold': 0,
                'total_revenue': 0.0
            }
        
        sales_summary[code]['total_quantity_sold'] += quantity
        sales_summary[code]['total_revenue'] += t['revenue']
        
    # Sort by total quantity sold (descending)
    sorted_items = sorted(
        sales_summary.values(), 
        key=lambda x: x['total_quantity_sold'], 
        reverse=True
    )
    
    return sorted_items[:top_n]


# --- CRUD Operations ---

def add_product(inventory: List[Product], name: str, price: float, stock: int) -> Optional[Product]:
    name = name.strip()
    # Simple code generation: first three letters + inventory count
    item_code = name[:3].upper() + str(len(inventory) + 1).zfill(3)
    
    if price <= 0 or stock < 0 or find_product(inventory, item_code):
        return None

    new_product = Product(item_code, name, price, stock)
    inventory.append(new_product)
    return new_product

def update_product_details(inventory: List[Product], item_code: str, adjustment_quantity: Optional[int] = None, new_price: Optional[float] = None) -> bool:
    """
    Stock Adjustment: Updates the stock (via adjustment) and/or price of an existing product.
    adjustment_quantity is the amount to add or subtract (e.g., +20 or -5).
    """
    product = find_product(inventory, item_code)
    
    if not product:
        return False
        
    if adjustment_quantity is not None:
        if product.stock + adjustment_quantity < 0:
            return False 
        
        product.stock += adjustment_quantity
        
    if new_price is not None:
        if new_price <= 0: return False
        product.price = new_price
        
    return True

def delete_product(inventory: List[Product], item_code: str) -> bool:
    product = find_product(inventory, item_code)
    if product:
        inventory[:] = [p for p in inventory if p.item_code != item_code]
        return True
    return False

# --- User I/O and Management (CLEANED) ---

def load_users() -> list:
    """Loads user data from the JSON file."""
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, 'r') as f:
            data = json.load(f)
            # Keys have been simplified for local login only
            return [User(
                item['id'], 
                item['username'], 
                item.get('password_hash')
            ) for item in data]
    except (IOError, json.JSONDecodeError):
        return []

def save_users(users: list):
    """Saves the current users list to the JSON file."""
    data = [u.to_dict() for u in users]
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        print("Error: Could not save users file.")

def get_user_by_id(user_id: str) -> Optional[User]:
    """Finds a user by their unique ID for Flask-Login user_loader."""
    users = load_users()
    return next((u for u in users if u.id == user_id), None)

def get_user_by_username(username: str) -> Optional[User]:
    """Finds a user by their unique username for local login/signup check."""
    users = load_users()
    return next((u for u in users if u.username == username.strip()), None)

# NOTE: get_user_by_google_id and add_user_from_oauth removed.

def add_user(username: str, password: str) -> Optional[User]:
    """Creates a new user with a hashed password (for local signup)."""
    if get_user_by_username(username):
        return None # User already exists

    users = load_users()
    new_id = str(len(users) + 1)
    
    password_hash = generate_password_hash(password)
    
    new_user = User(new_id, username, password_hash=password_hash)
    users.append(new_user)
    save_users(users)
    
    return new_user