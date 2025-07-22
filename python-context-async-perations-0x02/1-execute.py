import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_name='users.db'):
        """
        Initialize the context manager with query and parameters
        
        Args:
            query (str): SQL query to execute
            params (tuple or list): Parameters for the query (optional)
            db_name (str): Database name (defaults to 'users.db')
        """
        self.query = query
        self.params = params or ()
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """
        Open connection, execute query, and return results
        """
        print(f"Opening database connection to {self.db_name}")
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
        try:
            print(f"Executing query: {self.query}")
            if self.params:
                print(f"With parameters: {self.params}")
                self.cursor.execute(self.query, self.params)
            else:
                self.cursor.execute(self.query)
            
            # Fetch results based on query type
            if self.query.strip().upper().startswith('SELECT'):
                self.results = self.cursor.fetchall()
                print(f"Query returned {len(self.results)} rows")
            else:
                # For INSERT, UPDATE, DELETE operations
                self.results = self.cursor.rowcount
                print(f"Query affected {self.results} rows")
            
            return self.results
            
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Clean up resources and handle exceptions
        """
        if self.connection:
            if exc_type is not None:
                # If an exception occurred, rollback any uncommitted changes
                print(f"Exception occurred: {exc_type.__name__}: {exc_val}")
                self.connection.rollback()
                print("Transaction rolled back")
            else:
                # If no exception, commit any pending changes
                self.connection.commit()
                print("Transaction committed")
            
            # Close cursor and connection
            if self.cursor:
                self.cursor.close()
            
            print(f"Closing database connection to {self.db_name}")
            self.connection.close()
        
        # Return False to propagate any exceptions
        return False

# Example usage: Execute query with parameters
print("=== Executing query with parameters ===")
with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print("Query results:")
    for row in results:
        print(row)

print("\n=== Executing simple query without parameters ===")
with ExecuteQuery("SELECT * FROM users") as results:
    print("All users:")
    for row in results:
        print(row)

print("\n=== Example with UPDATE query ===")
with ExecuteQuery("UPDATE users SET status = ? WHERE age > ?", ('active', 30)) as affected_rows:
    print(f"Updated {affected_rows} rows")