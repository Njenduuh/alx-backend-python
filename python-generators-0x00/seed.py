import mysql.connector
from mysql.connector import Error
import csv
import uuid

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="willie@50"  # ✅ Your MySQL root password
        )
        return connection
    except Error as e:
        print(f"Connection error: {e}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists.")
    except Error as e:
        print(f"Database creation error: {e}")
    finally:
        cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="willie@50",  # ✅ Your password here too
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Connection to ALX_prodev error: {e}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Table creation error: {e}")
    finally:
        cursor.close()

def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = row.get("user_id") or str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (user_id,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully.")
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found.")
    except Error as e:
        print(f"Insert error: {e}")
    finally:
        cursor.close()
