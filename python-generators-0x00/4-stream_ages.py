#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.

    Returns:
        connection: MySQL connection object to ALX_prodev database or None if connection fails
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


def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database.

    Yields:
        int: Individual user age
    """
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        # Loop 1: Fetch and yield ages one by one
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]  # row[0] is the age value

    except Error as e:
        print(f"Error streaming user ages: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def calculate_average_age():
    """
    Calculate the average age of users using the generator.
    This function computes the average without loading all data into memory.

    Returns:
        float: Average age of users
    """
    total_age = 0
    user_count = 0

    # Loop 2: Process each age from the generator
    for age in stream_user_ages():
        total_age += age
        user_count += 1

    if user_count == 0:
        return 0

    return total_age / user_count


if __name__ == "__main__":
    # Calculate and print the average age
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")
