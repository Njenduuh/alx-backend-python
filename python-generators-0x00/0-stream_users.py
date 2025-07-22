#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.

    Yields:
        dict: Each row from the user_data table as a dictionary with keys:
              'user_id', 'name', 'email', 'age'
    """
    connection = None
    cursor = None

    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='willie@50',  # ✅ Updated password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Returns rows as dictionaries
            cursor.execute("SELECT user_id, name, email, age FROM user_data")

            # Single loop as required - fetch and yield one row at a time
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row

    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return

    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
