import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from function arguments
        # Check if 'query' is in kwargs first, then check positional args
        query = None
        if 'query' in kwargs:
            query = kwargs['query']
        elif args:
            # Assuming the first argument is the query (adjust index if needed)
            query = args[0]
        
        # Log the query
        if query:
            print(f"[SQL QUERY LOG] Executing: {query}")
        else:
            print("[SQL QUERY LOG] No query parameter found")
        
        # Execute the original function
        return func(*args, **kwargs)
    
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")