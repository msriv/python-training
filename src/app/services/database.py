# src/app/services/database.py

import mysql.connector
from mysql.connector import pooling
from mysql.connector import errorcode
from ...config.settings import Settings # Import the Settings singleton

# --- Global Variables ---
# _db_pool will hold the single instance of the connection pool object
_db_pool = None 

# --- Constants ---
# Define the size of your connection pool
POOL_SIZE = 5 
# Define the connection type based on the scheme in the URI
# Since we are using mysql+pymysql, we'll assume standard MySQL connection 
# If you were using SQLAlchemy, the engine creation would be slightly different
DB_TYPE = "mysql" 


class DatabaseSingleton:
    """
    Singleton class to manage the global database connection pool.
    """
    _instance = None

    def __new__(cls):
        """Ensures only a single instance of DatabaseSingleton exists."""
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            # Initialize the connection pool only once
            cls._instance._initialize_pool()
        return cls._instance

    def _initialize_pool(self):
        """
        Creates the global MySQL connection pool using the URI from Settings.
        This method is called only once during application startup.
        """
        global _db_pool
        if _db_pool is not None:
            # Already initialized, should not happen in __new__ but good for safety
            return

        # 1. Get the database URI from the Settings singleton
        settings = Settings()
        db_uri = settings.db_uri
        
        # 2. Parse the URI to get individual connection parameters
        # Format: mysql+pymysql://user:password@host:port/database
        try:
            # Simple manual parsing of the URI string (for mysql.connector)
            # NOTE: For complex scenarios, use urllib.parse.urlparse
            parts = db_uri.split("://")[1].split("@")
            user_pass, host_port_db = parts[0], parts[1]
            
            user, password = user_pass.split(":")
            host_port, database = host_port_db.split("/")
            host, port = host_port.split(":")
            port = int(port)
            
            db_config = {
                'host': host,
                'user': user,
                'password': password,
                'database': database,
                'port': port,
            }
            
            print(f"Initializing {DB_TYPE} pool for database: {database}...")

            # 3. Create the Connection Pool
            _db_pool = pooling.MySQLConnectionPool(
                pool_name="ApplicationDBPool",
                pool_size=POOL_SIZE,
                **db_config
            )
            print(f"Database pool successfully initialized with size {POOL_SIZE}.")

        except Exception as e:
            print(f"FATAL ERROR: Failed to initialize DB connection pool. Check URI format or credentials.")
            print(f"Details: {e}")
            # Raise the exception to prevent the application from starting
            raise RuntimeError("Database connection failed during startup.")

    def get_connection(self):
        """
        Retrieves an active connection from the pool.
        The calling code MUST remember to call connection.close() to return 
        the connection to the pool.
        """
        if _db_pool is None:
            raise Exception("Database pool has not been initialized.")
        
        try:
            # This fetches a connection object from the pool
            return _db_pool.get_connection()
        except mysql.connector.Error as err:
            print(f"Error retrieving connection from pool: {err}")
            # Handle specific pool errors if necessary
            raise

    # Optional: A method to safely close all connections in the pool on shutdown
    def close_pool(self):
        """Closes all connections in the pool."""
        global _db_pool
        if _db_pool:
            _db_pool.close()
            _db_pool = None
            print("Database connection pool closed.")

# --- Usage Example (Demonstration) ---
if __name__ == '__main__':
    # 1. Get the singleton instance (initializes the pool)
    db_manager = DatabaseSingleton()
    
    print("\n--- Testing Connection Retrieval ---")
    
    conn1 = None
    conn2 = None
    
    try:
        # 2. Get connections from the pool
        conn1 = db_manager.get_connection()
        conn2 = db_manager.get_connection()
        
        print(f"Connection 1 is active: {conn1.is_connected()}")
        print(f"Connection 2 is active: {conn2.is_connected()}")
        
        # In a real scenario, you would execute a query here
        # Example: cursor = conn1.cursor(); cursor.execute("SELECT 1"); ...
        
    except Exception as e:
        print(f"Test failed: {e}")
        
    finally:
        # 3. Connections MUST be closed to return them to the pool
        if conn1:
            conn1.close()
            print("Connection 1 returned to pool.")
        if conn2:
            conn2.close()
            print("Connection 2 returned to pool.")
            
    # 4. Cleanup when the app is shutting down
    # db_manager.close_pool()