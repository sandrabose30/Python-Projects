#Online shopping management system

import sqlite3
from datetime import datetime

DB_NAME = "online_shopping.db"


def get_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"[-] Database connection error: {e}")
        return None


def initialize_database():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('Admin', 'Customer')) NOT NULL,
                email TEXT UNIQUE NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL CHECK(price >= 0),
                stock INTEGER NOT NULL CHECK(stock >= 0)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                total_price REAL NOT NULL,
                order_date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
            );
        """)

        cursor.execute("SELECT COUNT(*) FROM users;")
        if cursor.fetchone()[0] == 0:
            sample_users = [
                ("admin_root", "admin123", "Admin", "admin1@shop.com"),
                ("admin_sarah", "sarah123", "Admin", "sarah.admin@shop.com"),
                ("john_doe", "pass123", "Customer", "john@gmail.com"),
                ("alice_smith", "pass123", "Customer", "alice@gmail.com"),
                ("bob_jones", "pass123", "Customer", "bob@gmail.com"),
                ("charlie_brown", "pass123", "Customer", "charlie@gmail.com"),
                ("diana_prince", "pass123", "Customer", "diana@gmail.com"),
                ("ethan_hunt", "pass123", "Customer", "ethan@gmail.com"),
                ("fiona_gally", "pass123", "Customer", "fiona@gmail.com"),
                ("george_clark", "pass123", "Customer", "george@gmail.com")
            ]
            cursor.executemany("""
                INSERT INTO users (username, password, role, email)
                VALUES (?, ?, ?, ?);
            """, sample_users)

            sample_products = [
                ("Wireless Mouse", "Ergonomic optical mouse", 799.00, 50),
                ("Mechanical Keyboard", "RGB backlit gaming keyboard", 2499.00, 30),
                ("Type-C Cable", "Fast charging 1m cable", 299.00, 100),
                ("Gaming Headset", "Surround sound with mic", 1599.00, 25),
                ("Laptop Stand", "Adjustable aluminum stand", 899.00, 40)
            ]
            cursor.executemany("""
                INSERT INTO products (name, description, price, stock)
                VALUES (?, ?, ?, ?);
            """, sample_products)

            conn.commit()
            print("[+] Database initialized successfully with 10 default users and sample products.")

    except sqlite3.Error as e:
        print(f"[-] Error during database initialization: {e}")
    finally:
        conn.close()

def get_validated_input(prompt, data_type=str, condition=lambda x: True, error_msg="Invalid input."):
    while True:
        try:
            val = data_type(input(prompt).strip())
            if isinstance(val, str) and not val:
                print("[-] Input cannot be empty. Please try again.")
                continue
            if condition(val):
                return val
            else:
                print(f"[-] {error_msg}")
        except ValueError:
            print(f"[-] Invalid data type. Expected {data_type.__name__}.")

def register_user():
    print("\n--- User Registration ---")
    username = get_validated_input("Enter username: ")
    password = get_validated_input("Enter password: ")
    email = get_validated_input("Enter email: ")
    role = get_validated_input("Enter role (Admin/Customer): ", str, lambda r: r in ['Admin', 'Customer'],
                               "Role must be 'Admin' or 'Customer'.")

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?);",
                       (username, password, role, email))
        conn.commit()
        print("[+] Registration successful! You can now log in.")
    except sqlite3.IntegrityError:
        print("[-] Registration failed: Username or Email already exists.")
    except sqlite3.Error as e:
        print(f"[-] Database error: {e}")
    finally:
        conn.close()


def login_user(expected_role):
    print(f"\n--- {expected_role} Login ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id, username, role FROM users WHERE username = ? AND password = ? AND role = ?;",
                       (username, password, expected_role))
        user = cursor.fetchone()
        if user:
            print(f"\n[+] Login successful! Welcome, {user[1]} (Role: {user[2]})")
            return {"user_id": user[0], "username": user[1], "role": user[2]}
        else:
            print(f"[-] Invalid credentials or account is not a {expected_role}.")
            return None
    except sqlite3.Error as e:
        print(f"[-] Database error: {e}")
        return None
    finally:
        conn.close()

def admin_menu(current_user):
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. View All Products")
        print("2. Add New Product (Create)")
        print("3. Update Product Details (Update)")
        print("4. Delete Product (Delete)")
        print("5. View All Customer Orders")
        print("6. Logout")

        choice = get_validated_input("Select an option (1-6): ", int, lambda x: 1 <= x <= 6, "Choose between 1 and 6.")

        if choice == 1:
            view_products()
        elif choice == 2:
            add_product()
        elif choice == 3:
            update_product()
        elif choice == 4:
            delete_product()
        elif choice == 5:
            view_all_orders()
        elif choice == 6:
            print("[+] Logging out...")
            break


def view_products():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT product_id, name, description, price, stock FROM products;")
        products = cursor.fetchall()
        print("\n--- Product Catalog ---")
        print(f"{'ID':<5} | {'Name':<22} | {'Price (INR)':<12} | {'Stock':<6} | {'Description'}")
        print("-" * 75)
        for p in products:
            print(f"{p[0]:<5} | {p[1]:<22} | ₹{p[3]:<11.2f} | {p[4]:<6} | {p[2]}")
    except sqlite3.Error as e:
        print(f"[-] Error fetching products: {e}")
    finally:
        conn.close()


def add_product():
    print("\n--- Add New Product ---")
    name = get_validated_input("Product Name: ")
    description = get_validated_input("Description: ")
    price = get_validated_input("Price (INR): ", float, lambda x: x >= 0, "Price cannot be negative.")
    stock = get_validated_input("Stock Quantity: ", int, lambda x: x >= 0, "Stock cannot be negative.")

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?);",
                       (name, description, price, stock))
        conn.commit()
        print("[+] Product added successfully!")
    except sqlite3.Error as e:
        print(f"[-] Database error: {e}")
    finally:
        conn.close()


def update_product():
    view_products()
    product_id = get_validated_input("\nEnter Product ID to update: ", int, lambda x: x > 0, "Invalid ID.")

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM products WHERE product_id = ?;", (product_id,))
        if not cursor.fetchone():
            print("[-] Product ID not found.")
            return

        print("1. Update Price\n2. Update Stock\n3. Update Both")
        opt = get_validated_input("Choose option: ", int, lambda x: x in [1, 2, 3], "Invalid option.")

        if opt == 1 or opt == 3:
            new_price = get_validated_input("Enter new price: ", float, lambda x: x >= 0)
            cursor.execute("UPDATE products SET price = ? WHERE product_id = ?;", (new_price, product_id))
        if opt == 2 or opt == 3:
            new_stock = get_validated_input("Enter new stock quantity: ", int, lambda x: x >= 0)
            cursor.execute("UPDATE products SET stock = ? WHERE product_id = ?;", (new_stock, product_id))

        conn.commit()
        print("[+] Product updated successfully!")
    except sqlite3.Error as e:
        print(f"[-] Database error: {e}")
    finally:
        conn.close()


def delete_product():
    view_products()
    product_id = get_validated_input("\nEnter Product ID to delete: ", int, lambda x: x > 0, "Invalid ID.")

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE product_id = ?;", (product_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print("[+] Product deleted successfully.")
        else:
            print("[-] Product ID not found.")
    except sqlite3.Error as e:
        print(f"[-] Database error: {e}")
    finally:
        conn.close()


def view_all_orders():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT o.order_id, u.username, p.name, o.quantity, o.total_price, o.order_date
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            JOIN products p ON o.product_id = p.product_id;
        """)
        orders = cursor.fetchall()
        print("\n--- All Customer Orders ---")
        if not orders:
            print("No orders have been placed yet.")
            return
        print(f"{'Ord ID':<7} | {'Customer':<15} | {'Product':<20} | {'Qty':<4} | {'Total (INR)':<10} | {'Date'}")
        print("-" * 75)
        for o in orders:
            print(f"{o[0]:<7} | {o[1]:<15} | {o[2]:<20} | {o[3]:<4} | ₹{o[4]:<9.2f} | {o[5]}")
    except sqlite3.Error as e:
        print(f"[-] Database error: {e}")
    finally:
        conn.close()


def customer_menu(current_user):
    while True:
        print(f"\n--- Customer Dashboard ({current_user['username']}) ---")
        print("1. Browse Products & Place Order")
        print("2. View My Order History")
        print("3. Logout")

        choice = get_validated_input("Select an option (1-3): ", int, lambda x: 1 <= x <= 3, "Choose between 1 and 3.")

        if choice == 1:
            place_order(current_user['user_id'])
        elif choice == 2:
            view_my_orders(current_user['user_id'])
        elif choice == 3:
            print("[+] Logging out...")
            break


def place_order(user_id):
    view_products()
    product_id = get_validated_input("\nEnter Product ID to purchase: ", int, lambda x: x > 0, "Invalid ID.")

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT price, stock FROM products WHERE product_id = ?;", (product_id,))
        prod = cursor.fetchone()
        if not prod:
            print("[-] Product not found.")
            return

        price, stock = prod[0], prod[1]
        if stock <= 0:
            print("[-] Sorry, product is out of stock.")
            return

        qty = get_validated_input(f"Enter quantity (Available: {stock}): ", int,
                                  lambda x: 0 < x <= stock, f"Quantity must be between 1 and {stock}.")

        total_price = price * qty
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO orders (user_id, product_id, quantity, total_price, order_date)
            VALUES (?, ?, ?, ?, ?);
        """, (user_id, product_id, qty, total_price, order_date))

        cursor.execute("""
            UPDATE products SET stock = stock - ? WHERE product_id = ?;
        """, (qty, product_id))

        conn.commit()
        print(f"[+] Order placed successfully! Total Cost: ₹{total_price:.2f}")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"[-] Transaction failed: {e}")
    finally:
        conn.close()


def view_my_orders(user_id):
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT o.order_id, p.name, o.quantity, o.total_price, o.order_date
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE o.user_id = ?;
        """, (user_id,))
        orders = cursor.fetchall()
        print("\n--- My Order History ---")
        if not orders:
            print("You have not placed any orders yet.")
            return
        print(f"{'Ord ID':<7} | {'Product':<20} | {'Qty':<4} | {'Total (INR)':<10} | {'Date'}")
        print("-" * 65)
        for o in orders:
            print(f"{o[0]:<7} | {o[1]:<20} | {o[2]:<4} | ₹{o[3]:<9.2f} | {o[4]}")
    except sqlite3.Error as e:
        print(f"[-] Database error: {e}")
    finally:
        conn.close()

def main():
    initialize_database()
    while True:
        print("\n========================================")
        print("   ONLINE SHOPPING MANAGEMENT SYSTEM    ")
        print("========================================")
        print("1. Login")
        print("2. Register New User")
        print("3. Exit")

        choice = get_validated_input("Select an option (1-3): ", int, lambda x: 1 <= x <= 3, "Choose between 1 and 3.")

        if choice == 1:
            while True:
                print("\n--- Select Login Role ---")
                print("1. Admin Login")
                print("2. Customer Login")
                print("3. Back to Main Menu")

                role_choice = get_validated_input("Select role type (1-3): ", int, lambda x: 1 <= x <= 3,
                                                  "Choose between 1 and 3.")

                if role_choice == 1:
                    user = login_user("Admin")
                    if user:
                        admin_menu(user)
                        break
                elif role_choice == 2:
                    user = login_user("Customer")
                    if user:
                        customer_menu(user)
                        break
                elif role_choice == 3:
                    break
        elif choice == 2:
            register_user()
        elif choice == 3:
            print("\nThank you for using Online Shopping Management System. Goodbye!")
            break


if __name__ == "__main__":
    main()