#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
import csv
import uuid
import os


def connect_db():
    """
    Connects to the MySQL database server.
    Returns:
        connection: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='willie@50'  # ✅ Updated password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created successfully or already exists")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    Returns:
        connection: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='willie@50',  # ✅ Updated password
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file_path):
    """
    Inserts data from CSV file into the database if it does not exist.
    Uses a generator to efficiently process large CSV files.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"Data already exists in user_data table ({count} rows)")
            cursor.close()
            return

        def read_csv_data(file_path):
            """Generator that yields rows from CSV file one by one"""
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if 'user_id' not in row or not row['user_id']:
                            row['user_id'] = str(uuid.uuid4())
                        yield (
                            row['user_id'],
                            row['name'],
                            row['email'],
                            int(row['age'])
                        )
            except FileNotFoundError:
                print(f"Error: CSV file '{file_path}' not found")
                return
            except Exception as e:
                print(f"Error reading CSV file: {e}")
                return

        insert_query = """
        INSERT IGNORE INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """

        inserted_count = 0
        for user_data in read_csv_data(csv_file_path):
            cursor.execute(insert_query, user_data)
            inserted_count += 1
            if inserted_count % 1000 == 0:
                connection.commit()
                print(f"Inserted {inserted_count} rows...")

        connection.commit()
        cursor.close()
        print(f"Data insertion completed. Total rows inserted: {inserted_count}")

    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()


def stream_users_data(connection):
    """
    Generator that streams user data from the database one row at a time.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row

        cursor.close()

    except Error as e:
        print(f"Error streaming data: {e}")


def stream_users_data_paginated(connection, page_size=1000):
    """
    Generator that streams user data in paginated chunks for better memory efficiency.
    """
    try:
        cursor = connection.cursor()
        offset = 0

        while True:
            query = f"SELECT user_id, name, email, age FROM user_data LIMIT {page_size} OFFSET {offset}"
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                break

            for row in rows:
                yield row

            offset += page_size

        cursor.close()

    except Error as e:
        print(f"Error streaming paginated data: {e}")


if __name__ == "__main__":
    print("Testing database setup...")

    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()
        print("Initial connection successful")

        conn = connect_to_prodev()
        if conn:
            create_table(conn)

            if os.path.exists('user_data.csv'):
                insert_data(conn, 'user_data.csv')

                print("\nTesting generator - first 3 rows:")
                count = 0
                for user in stream_users_data(conn):
                    print(user)
                    count += 1
                    if count >= 3:
                        break

            conn.close()
        else:
            print("Failed to connect to ALX_prodev database")
    else:
        print("Failed to connect to MySQL server")
