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

4.Planned Feature: Secure Password Recovery
Future Development: The application currently lacks a "Forgot Password" mechanism. A critical future feature will be the implementation of a secure password recovery system. This will involve generating a unique, time-sensitive token and sending it to the user's registered email, allowing them to safely reset their password without intervention from an administrator. This is essential for user accessibility and security best practices.

# Installation and setup

Prerequisites
Ensure the user has these core tools installed on their system before proceeding:

Python 3.x: (Used for the backend logic and running the Flask application.)

pip: (Python package installer, typically included with Python.)

Git: (To clone the repository from your host, e.g., GitHub.)

# Step-by-Step Guide
Follow these steps to get the application running on your local machine:

1.Clone the Repository Open your terminal or command prompt and download the project files:

      git clone [YOUR_REPOSITORY_URL_HERE]
      cd product-inventory-manager
      
2.Set up a Virtual Environment (Recommended) Creating a virtual environment isolates your project dependencies from your main Python installation, preventing conflicts.

      python -m venv venv
      source venv/bin/activate    # On Linux/macOS
       .\venv\Scripts\activate     # On Windows Command Prompt

3.Install Required Libraries Install the Flask library, which is necessary to run the web application:

       pip install Flask

4.Run the Application Execute the main application file. The system will automatically create the database.db file and populate it with initial product data upon the first run.

       python app.py

# Technical Details & Architecture
1.Technology Stack

This lists the core tools and languages used to build the application:

Backend Language: Python 3.x

Web Framework: Flask (lightweight and minimal web application framework)

  [Project Root Folder]

  ├── .gitignore

  ├── app.py

  ├── database.db

  ├── inventory_data.json

  ├── inventory_manager.py

  ├── Procfile

  ├── requirements.txt

  ├── transactions_data.json

  ├── users_data.json

  ├── static/

  │   └── style.css

  └── templates/

├── add.html
    
├── base.html
    
├── best_sellers.html
    
├── index.html
    
├── login.html
    
├── sell.html
    
 ├── signup.html
    
└── update.html

# Link to access

https://optistock-c4j8.onrender.com

# Screenshots
<img width="1600" height="864" alt="image" src="https://github.com/user-attachments/assets/91caed30-7468-42d4-95dd-c256fc6ff081" />
<img width="1600" height="851" alt="image" src="https://github.com/user-attachments/assets/e69ee6fb-566a-42da-b042-4c27b5961613" />
<img width="1600" height="851" alt="image" src="https://github.com/user-attachments/assets/896e7339-a748-4ea5-9520-b85d5bdfba2d"/>
<img width="1600" height="851" alt="image" src="https://github.com/user-attachments/assets/2efd82fb-6460-4a6d-9218-590abc65245a"/>
<img width="1600" height="851" alt="image" src="https://github.com/user-attachments/assets/9d12d477-0502-449b-9a73-1cb6b37b48f8"/>

# Author
Ritika Gupta


















