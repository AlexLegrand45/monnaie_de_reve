import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',        # Replace with your host
            user='yourusername',     # Replace with your MySQL username
            password='yourpassword'  # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS online_bank")
        print("Database created successfully")
    except Error as e:
        print(f"Error: {e}")

def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("USE online_bank")

        # Create Users Table with Level Attribute
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            level ENUM('Basic', 'Premium', 'VIP') DEFAULT 'Basic',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Create Accounts Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            account_number VARCHAR(20) NOT NULL UNIQUE,
            balance DECIMAL(10, 2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')

        # Create UD_account Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ud_account (
            ud_account_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT UNIQUE,
            account_number VARCHAR(20) NOT NULL UNIQUE,
            balance DECIMAL(10, 2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        ''')

        # Create Transactions Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT,
            transaction_type ENUM('deposit', 'withdrawal', 'transfer') NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(account_id)
        )
        ''')

        print("Tables created successfully")
    except Error as e:
        print(f"Error: {e}")

def insert_sample_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("USE online_bank")

        # Insert sample user
        cursor.execute('''
        INSERT INTO users (username, password, email, level)
        VALUES ('john_doe', 'password123', 'john@example.com', 'Premium')
        ''')

        # Insert sample account
        cursor.execute('''
        INSERT INTO accounts (user_id, account_number, balance)
        VALUES (1, 'ACC123456789', 1000.00)
        ''')

        # Insert sample UD_account
        cursor.execute('''
        INSERT INTO ud_account (user_id, account_number, balance)
        VALUES (1, 'UDACC987654321', 500.00)
        ''')

        # Insert sample transactions
        cursor.execute('''
        INSERT INTO transactions (account_id, transaction_type, amount)
        VALUES (1, 'deposit', 500.00)
        ''')

        cursor.execute('''
        INSERT INTO transactions (account_id, transaction_type, amount)
        VALUES (1, 'withdrawal', 200.00)
        ''')

        connection.commit()
        print("Sample data inserted successfully")
    except Error as e:
        print(f"Error: {e}")

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

def main():
    connection = create_connection()
    if connection:
        create_database(connection)
        create_tables(connection)
        insert_sample_data(connection)
        close_connection(connection)

if __name__ == "__main__":
    main()
