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
            password='willie@50',  # ✅ Updated password here
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.
    
    Args:
        page_size (int): Number of users to fetch per page
        offset (int): Starting position for the page
        
    Returns:
        list: List of user dictionaries for the requested page
    """
    connection = connect_to_prodev()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Error as e:
        print(f"Error fetching paginated data: {e}")
        connection.close()
        return []


def lazy_paginate(page_size):
    """
    Generator function that lazily loads pages of user data.
    Only fetches the next page when needed, starting from offset 0.
    
    Args:
        page_size (int): Number of users per page
        
    Yields:
        list: A page of user records as dictionaries
    """
    offset = 0
    
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# Alias for the function name used in the test
lazy_pagination = lazy_paginate
