import time
import sqlite3 
import functools

# Database connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function with the connection as the first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close the connection, even if an exception occurs
            conn.close()
    
    return wrapper

query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from function arguments
        # Look for 'query' in kwargs first, then check positional args
        cache_key = None
        
        if 'query' in kwargs:
            cache_key = kwargs['query']
        elif len(args) > 1:  # Skip the first argument (conn) and look for query
            cache_key = args[1]
        
        # If we found a query, check if it's cached
        if cache_key and cache_key in query_cache:
            print(f"Cache hit for query: {cache_key}")
            return query_cache[cache_key]
        
        # Execute the function since result is not cached
        print(f"Cache miss for query: {cache_key}")
        result = func(*args, **kwargs)
        
        # Cache the result if we have a cache key
        if cache_key:
            query_cache[cache_key] = result
            print(f"Result cached for query: {cache_key}")
        
        return result
    
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")