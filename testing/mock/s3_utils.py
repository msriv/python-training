import boto3
import pandas as pd
import io

# We assume 's3_client' is initialized here or passed in.
# For simplicity, we initialize it globally, which is common.
s3_client = boto3.client('s3')

def load_data_from_s3(bucket_name: str, key: str) -> pd.DataFrame:
    """Reads a CSV file from S3 into a pandas DataFrame."""
    try:
        # The key operation we need to mock is calling get_object() on the client
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        
        # Read the raw binary stream
        body = response['Body'].read()
        
        # Use io.BytesIO to treat the binary data as a file
        data_stream = io.BytesIO(body)
        
        # Load the data into a DataFrame
        df = pd.read_csv(data_stream)
        return df
        
    except Exception as e:
        print(f"Error reading from S3: {e}")
        return pd.DataFrame()