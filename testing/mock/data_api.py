import requests
import pandas as pd

API_ENDPOINT = 'http://api.externaldata.com/users'

def fetch_user_data(user_id):
    """Fetches user data from an external API and returns a DataFrame."""
    try:
        response = requests.get(f"{API_ENDPOINT}/{user_id}")
        response.raise_for_status()  # Raises an exception for bad status codes
        
        data = response.json().get('user_info', {})
        # Flatten and process data into a DataFrame
        return pd.DataFrame([data]) 
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return pd.DataFrame()