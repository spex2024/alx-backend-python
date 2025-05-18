import os
import csv
import uuid
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment Variables
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

DB_NAME = MYSQL_DATABASE
TABLE_NAME = 'user_data'

def get_connection(database=None):
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=database
    ) if database else mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )

def connect_db():
    try:
        conn = get_connection()
        print("✅ Connected to MySQL server.")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to MySQL server: {e}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✅ Database '{DB_NAME}' ensured.")
        cursor.close()
    except Exception as e:
        print(f"❌ Failed to create database: {e}")

def connect_to_prodev():
    try:
        conn = get_connection(DB_NAME)
        print(f"✅ Connected to database '{DB_NAME}'.")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to database {DB_NAME}: {e}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(query)
        connection.commit()
        print(f"✅ Table '{TABLE_NAME}' ensured.")
        cursor.close()
    except Exception as e:
        print(f"❌ Failed to create table: {e}")

def insert_data(connection, data):
    cursor = connection.cursor()
    for record in data:
        user_id = record.get('user_id') or str(uuid.uuid4())
        name = record['name']
        email = record['email']
        age = record['age']

        # Check if user_id exists
        cursor.execute(f"SELECT 1 FROM {TABLE_NAME} WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            print(f"⚠️ Skipping existing user_id {user_id}")
            continue

        insert_query = f"""
        INSERT INTO {TABLE_NAME} (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, name, email, age))
        print(f"✅ Inserted user: {name} ({user_id})")

    connection.commit()
    cursor.close()

def load_csv_data(csv_path):
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print(f"❌ File not found: {csv_path}")
        return []

if __name__ == "__main__":
    # Step 1: Connect without database to create it
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

        # Step 2: Connect to Alx_prodev database
        conn = connect_to_prodev()
        if conn:
            create_table(conn)
            # Step 3: Load and insert CSV data
            data = load_csv_data('data/user_data.csv')
            insert_data(conn, data)
            conn.close()
