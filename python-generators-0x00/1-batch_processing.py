#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows from the user_data table in batches.

    Args:
        batch_size (int): Number of rows to fetch in each batch

    Yields:
        list: A batch of user records as dictionaries
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
            cursor = connection.cursor(dictionary=True)
            offset = 0

            # Loop 1: Fetch data in batches using LIMIT and OFFSET
            while True:
                query = f"SELECT user_id, name, email, age FROM user_data LIMIT {batch_size} OFFSET {offset}"
                cursor.execute(query)
                batch = cursor.fetchall()

                if not batch:
                    break

                yield batch
                offset += batch_size

    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return

    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Process batches of users and filter those over the age of 25.

    Args:
        batch_size (int): Number of rows to process in each batch
    """
    # Loop 2: Process each batch from the generator
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Filter users over age 25 from each batch
        for user in batch:
            if user['age'] > 25:
                print(user)
