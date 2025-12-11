# OptiStock
OptiStock: A simple web app for managing product stock and sales records using flask and python.
# Project theme
The primary goal of your application is to ensure accurate and accessible inventory control by allowing quick management of product data. The core functionality centers around Product Maintenance, where you can update permanent details like the product Name and Price, and Stock Adjustments, which let you fix inventory counts for reasons other than sales, such as damage or counting errors. Technologically, the system operates on the standard CRUD (Create, Read, Update, Delete) pattern. When a user clicks "Edit," the system safely Reads (GET) the existing data. When they click "Save," it executes an Update (POST) operation, changing the details in the database. This clear separation of reading and writing data is a fundamental programming concept that helps keep your inventory records consistent and reliable.
# Features
1.Product Listing & Viewing:

The application displays a complete table of all inventory items.

Users can easily view the current Name, Price, and Stock for every product. (This is the fundamental Read operation).

2.Detailed Editing:

The system allows for the modification of permanent product details, including the Product Name and Selling Price.

The edit forms are pre-filled with the current data, improving the user experience.

3.Stock Adjustment & Correction:

Users can quickly and directly update the on-hand Stock Quantity.

This is crucial for performing Stock Adjustments to account for non-sale changes, such as damaged goods, losses, or correcting counting errors. (The editing and stock changes are handled by the Update operation of the CRUD pattern).
6. Planned Feature: Secure Password Recovery
Future Development: The application currently lacks a "Forgot Password" mechanism. A critical future feature will be the implementation of a secure password recovery system. This will involve generating a unique, time-sensitive token and sending it to the user's registered email, allowing them to safely reset their password without intervention from an administrator. This is essential for user accessibility and security best practices.
# installation and setup
Prerequisites
Ensure the user has these core tools installed on their system before proceeding:

Python 3.x: (Used for the backend logic and running the Flask application.)

pip: (Python package installer, typically included with Python.)

# Step-by-Step Guide
Follow these steps to get the application running on your local machine:

# Clone the Repository Open your terminal or command prompt and download the project files:

git clone [YOUR_REPOSITORY_URL_HERE]
cd product-inventory-manager
Set up a Virtual Environment (Recommended) Creating a virtual environment isolates your project dependencies from your main Python installation, preventing conflicts.

# Create the environment
python -m venv venv

# Activate the environment
source venv/bin/activate    # On Linux/macOS

# .\venv\Scripts\activate     # On Windows Command Prompt
Install Required Libraries Install the Flask library, which is necessary to run the web application:

pip install Flask
Run the Application Execute the main application file. The system will automatically create the database.db file and populate it with initial product data upon the first run.

python app.py

