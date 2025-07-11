import time
import sqlite3 
import functools

#### paste your with_db_decorator here
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

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(retries + 1):  # +1 to include the initial attempt
                try:
                    # Attempt to execute the function
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    # If this is the last attempt, raise the exception
                    if attempt == retries:
                        print(f"Function {func.__name__} failed after {retries + 1} attempts")
                        raise last_exception
                    
                    # Log the retry attempt
                    print(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}")
                    print(f"Retrying in {delay} seconds... ({attempt + 1}/{retries + 1})")
                    
                    # Wait before retrying
                    time.sleep(delay)
            
            # This should never be reached, but just in case
            raise last_exception
        
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)