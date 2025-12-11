from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import inventory_manager

app = Flask(__name__)
app.secret_key = 'Ritika@123' 

# flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_route'
login_manager.login_message_category = 'warning'
login_manager.login_message = ""  

@login_manager.user_loader
def load_user(user_id):
    users = inventory_manager.load_users()
    return next((u for u in users if u.id == user_id), None)

inventory = inventory_manager.load_inventory()

#AUTHENTICATION ROUTES 
@app.route('/signup', methods=['GET', 'POST'])
def signup_route():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        try:
            username = request.form['username'].strip()
            password = request.form['password']
            
            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'danger')
                return redirect(url_for('signup_route'))
    
            user = inventory_manager.add_user(username, password)
            
            if user:
                flash('Account created successfully! Please log in.', 'success')
                return redirect(url_for('login_route'))
            else:
                flash('Username already exists.', 'danger')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = inventory_manager.get_user_by_username(username)
        
        if user and user.password_hash and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required 
def logout_route():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login_route'))

#PROTECTED INVENTORY ROUTES

@app.route('/')
@login_required 
def index():
    
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        # Filter inventory based on item_code or name
        filtered_inventory = [
            p for p in inventory 
            if search_query.upper() in p.item_code.upper() or search_query.lower() in p.name.lower()
        ]
        flash(f"Showing results for '{search_query}'.", 'info')
    else:
        filtered_inventory = inventory
    
    sorted_inventory = sorted(filtered_inventory, key=lambda p: p.item_code)
    
    total_value = inventory_manager.get_total_inventory_value(filtered_inventory)
    low_stock = inventory_manager.get_low_stock_items(filtered_inventory)
    
    return render_template(
        'index.html',
        products=sorted_inventory,
        total_value=total_value,
        low_stock_count=len(low_stock),
        inventory_manager=inventory_manager,
        search_query=search_query
    )

@app.route('/add', methods=['GET', 'POST'])
@login_required 
def add_product_route():
    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            price = float(request.form['price'])
            stock = int(request.form['stock'])
            
            new_product = inventory_manager.add_product(inventory, name, price, stock)
            
            if new_product:
                inventory_manager.save_inventory(inventory)
                flash(f'Product {new_product.item_code} added successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Error: Product name might be a duplicate, or price/stock is invalid.', 'danger')
                
        except ValueError:
            flash('Error: Invalid number format for price or stock.', 'danger')
        except Exception as e:
            flash(f'An unexpected error occurred: {e}', 'danger')

    return render_template('add.html')

@app.route('/sell', methods=['GET', 'POST'])
@login_required 
def record_sale_route():
    if request.method == 'POST':
        try:
            item_code = request.form['item_code'].strip().upper()
            quantity = int(request.form['quantity'])
            
            transaction = inventory_manager.record_sale(inventory, item_code, quantity)
            
            if transaction:
                inventory_manager.save_inventory(inventory) 
                flash(f'Sale of {transaction["quantity"]} x {transaction["name"]} recorded! Stock updated.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Error: Product not found, invalid quantity, or insufficient stock.', 'danger')
                
        except ValueError:
            flash('Error: Quantity must be a valid whole number.', 'danger')
        except Exception as e:
            flash(f'An unexpected error occurred: {e}', 'danger')

    return render_template('sell.html')

@app.route('/update/<item_code>', methods=['GET', 'POST'])
@login_required 
def update_product_route(item_code):
    product = inventory_manager.find_product(inventory, item_code)
    
    if not product:
        flash(f'Product {item_code} not found.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            adjustment_input = request.form.get('adjustment_quantity').strip()
            adjustment_value = int(adjustment_input) if adjustment_input else None
            
            new_price_input = request.form.get('price').strip()
            price_value = float(new_price_input) if new_price_input else None

            if inventory_manager.update_product_details(inventory, item_code, adjustment_value, price_value):
                inventory_manager.save_inventory(inventory)
                flash(f'Product {item_code} updated successfully!', 'success')
            else:
                flash('Error: Invalid adjustment or price value, or stock would become negative.', 'danger')

            return redirect(url_for('index'))

        except ValueError:
            flash('Error: Invalid number format for stock adjustment or price.', 'danger')
        
    return render_template('update.html', product=product)

@app.route('/delete/<item_code>')
@login_required 
def delete_product_route(item_code):
    if inventory_manager.delete_product(inventory, item_code):
        inventory_manager.save_inventory(inventory)
        flash(f'Product {item_code} deleted successfully!', 'warning')
    else:
        flash(f'Error: Product {item_code} not found.', 'danger')
        
    return redirect(url_for('index'))


# REPORTING ROUTE
@app.route('/reports/best-sellers')
@login_required
def best_sellers_route():
    """Displays the top N products sold based on transaction data."""
    transactions = inventory_manager.load_transactions()
    best_sellers = inventory_manager.get_best_selling_items(transactions, top_n=5)
    
    return render_template('best_sellers.html', best_sellers=best_sellers)


if __name__ == '__main__':
    app.run(debug=True)