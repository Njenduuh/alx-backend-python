seed.py script that meets all your requirements. Here's what the script includes:
Core Functions (as requested):

connect_db() - Connects to the MySQL database server
create_database(connection) - Creates the ALX_prodev database if it doesn't exist
connect_to_prodev() - Connects specifically to the ALX_prodev database
create_table(connection) - Creates the user_data table with the required fields
insert_data(connection, data) - Inserts data from CSV file if it doesn't exist

Key Features:
Database Schema:

user_id (Primary Key, VARCHAR(36) for UUID, Indexed)
name (VARCHAR, NOT NULL)
email (VARCHAR, NOT NULL)
age (DECIMAL, NOT NULL)

Generator Implementation:

stream_users_data(connection) - Main generator that streams rows one by one
read_csv_data(file_path) - Generator for reading CSV data efficiently
stream_users_data_paginated(connection, page_size) - Alternative generator with pagination for large datasets

Additional Features:

Error handling for database connections and operations
UUID generation for user_id if not present in CSV
Batch processing for better performance during inserts
Duplicate prevention using INSERT IGNORE
Memory efficient streaming using generators

Usage:

Update database credentials in the script (username/password)
Ensure you have the user_data.csv file in the same directory
Run with your test script as shown in your example