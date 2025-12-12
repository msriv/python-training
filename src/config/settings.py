import os
import boto3
import json
from dotenv import load_dotenv

# Path to load the .env file (executed only once on module load)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env'))

class Settings:
    _instance = None
    
    # Static variable to hold the fetched secret string to prevent re-fetching
    _db_uri = None 

    def __new__(cls):
        """Ensures only a single instance of Settings exists and initializes it once."""
        if cls._instance is None:
            # --- Initialization block (Executed only once) ---
            cls._instance = super(Settings, cls).__new__(cls)
            
            # 1. Determine environment once
            cls._instance.env = os.getenv('APP_ENV', 'prod')
            
            # 2. Lazily fetch DB URI once and store it
            cls._instance._db_uri = cls._instance._get_db_uri()
            
        return cls._instance

    # Using a property decorator allows accessing the URI via Settings().db_uri
    @property
    def db_uri(self):
        """Public accessor for the database URI."""
        return self._db_uri

    def _get_db_uri(self):
        """Generates the DB URI based on the environment."""
        if self.env == 'dev':
            # ... (SQLite logic remains the same) ...
            db_file = os.getenv('SQLITE_DB_FILE', 'dev.db')
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'processed', db_file)
            db_path = os.path.normpath(db_path)
            return f'sqlite:///{db_path}'
            
        elif self.env == 'prod':
            secret_name = os.getenv('MYSQL_SECRET_NAME')
            region_name = os.getenv('AWS_REGION')
            
            if not secret_name or not region_name:
                raise EnvironmentError("MYSQL_SECRET_NAME or AWS_REGION not set for 'prod' environment.")
                
            creds = self._get_mysql_credentials_from_aws(secret_name, region_name)
            
            if creds:
                # Use os.path.get to safely access the dictionary keys with default values
                host = creds.get('host')
                user = creds.get('username')
                password = creds.get('password')
                port = creds.get('port', 3306)
                database = creds.get('database')
                
                # Basic check for essential credentials
                if not all([host, user, password, database]):
                    raise ValueError("Secrets Manager payload is missing essential keys (host, username, password, or database).")
                    
                return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
            else:
                # The exception is now raised from _get_mysql_credentials_from_aws, 
                # but we keep this check for clarity.
                raise Exception('Could not fetch MySQL credentials from AWS Secrets Manager')
                
        else:
            raise ValueError(f"Unknown environment: {self.env}")

    def _get_mysql_credentials_from_aws(self, secret_name, region_name):
        """Fetches and parses credentials from Secrets Manager."""
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        except Exception as e:
            # Raise a specific error that explains the failure context
            raise RuntimeError(f"AWS Secrets Manager failed to retrieve secret '{secret_name}': {e}") from e

# Example usage (import Settings and use Settings().db_uri)
if __name__ == '__main__':
    # The first call initializes the secrets
    settings1 = Settings()
    print(f"URI 1: {settings1.db_uri}")
    
    # The second call returns the same instance without re-fetching secrets
    settings2 = Settings()
    print(f"URI 2: {settings2.db_uri}")
    
    print(f"Are instances the same? {settings1 is settings2}") # Should be True