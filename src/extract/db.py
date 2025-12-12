# src/extract/db_extractor.py

from ..app.services.database import DatabaseSingleton
import pandas as pd

def extract_latest_data():
    """Extracts data using a connection from the singleton pool."""
    conn = None
    try:
        # 1. Get the connection manager instance
        db_manager = DatabaseSingleton()
        
        # 2. Get a fresh connection from the pool
        conn = db_manager.get_connection() 
        
        query = "SELECT * FROM house_prices;"
        
        # 3. Use Pandas to read data
        df = pd.read_sql(query, conn)
        
        print(f"Successfully extracted {len(df)} rows.")
        return df
        
    except Exception as e:
        print(f"Extraction failed: {e}")
        # Reraise or handle the exception specific to the extraction component
        raise
        
    finally:
        # 4. IMPORTANT: Always close the connection to return it to the pool
        if conn:
            conn.close() 
            # Note: This does NOT close the physical connection; it returns it to the pool for reuse.

if __name__ == '__main__':
    print(extract_latest_data())