import mysql.connector
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialize Faker
fake = Faker()

def create_database():
    # Connect to MySQL server (change these credentials as needed)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Using root as the username
        password="root"   # Using the confirmed working password
    )
    cursor = conn.cursor()

    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS my_store")
    cursor.execute("USE my_store")

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        total_amount DECIMAL(10,2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    return conn, cursor

def insert_sample_data(cursor, num_users=100, max_orders_per_user=10):
    # Insert users
    for _ in range(num_users):
        name = fake.name()
        email = fake.email()
        try:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (name, email)
            )
        except mysql.connector.IntegrityError:
            # Skip if email already exists
            continue

    # Get all user IDs
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Insert orders
    for user_id in user_ids:
        # Random number of orders for each user
        num_orders = random.randint(0, max_orders_per_user)
        for _ in range(num_orders):
            # Generate random amount between 10 and 1000
            amount = round(random.uniform(10, 1000), 2)
            # Generate random date within last 6 months
            created_at = fake.date_time_between(
                start_date='-6m',
                end_date='now'
            ).strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute(
                "INSERT INTO orders (user_id, total_amount, created_at) VALUES (%s, %s, %s)",
                (user_id, amount, created_at)
            )

def main():
    try:
        print("Connecting to MySQL...")
        conn, cursor = create_database()
        
        print("Inserting sample data...")
        insert_sample_data(cursor)
        
        # Commit the changes
        conn.commit()
        
        # Print some statistics
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
        
        print(f"\nDatabase 'my_store' created successfully!")
        print(f"Inserted {user_count} users")
        print(f"Inserted {order_count} orders")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if "Access denied" in str(err):
            print("\nPlease make sure to:")
            print("1. Install MySQL if you haven't already")
            print("2. Update the username and password in the script")
            print("3. Make sure MySQL server is running")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("\nMySQL connection closed.")

if __name__ == "__main__":
    main()