import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from s3_utils import load_data_from_s3
import io

# Test data we want the mock to return, formatted as a CSV string
MOCK_CSV_CONTENT = (
    "id,name,value\n"
    "1,Alpha,100\n"
    "2,Beta,200\n"
    "3,Gamma,300\n"
)

# 💡 Fixture for the expected DataFrame
@pytest.fixture
def expected_s3_df():
    """Provides the DataFrame we expect from the mock CSV content."""
    data = {'id': [1, 2, 3], 'name': ['Alpha', 'Beta', 'Gamma'], 'value': [100, 200, 300]}
    return pd.DataFrame(data)


def test_load_data_from_s3_success(mocker, expected_s3_df):
    """
    Tests successful S3 data loading by mocking the Boto3 call.
    """
    
    # 1. ARRANGE: Configure the Mock Response
    
    # Boto3's response for get_object is a dictionary. The file content
    # is inside the 'Body' key, which is a streaming object with a .read() method.
    
    # Mock the 'Body' object
    mock_body = mocker.Mock()
    # Configure what mock_body.read() should return (the raw bytes of our CSV)
    mock_body.read.return_value = MOCK_CSV_CONTENT.encode('utf-8')
    
    # Configure the full get_object response dictionary
    mock_response = {'Body': mock_body}
    
    # 2. ARRANGE: Patch the Target Function
    
    # The real S3 client is imported as 's3_client' in s3_utils.py.
    # We are mocking the 'get_object' method *on* that client object.
    mock_get_object = mocker.patch(
        's3_utils.s3_client.get_object',
        return_value=mock_response
    )
    
    # 3. ACT: Call the Function Under Test
    test_bucket = 'test-pipeline-bucket'
    test_key = 'raw/data.csv'
    actual_df = load_data_from_s3(test_bucket, test_key)
    
    # 4. ASSERT: Verification
    
    # Check that the returned DataFrame matches the data we mocked
    assert_frame_equal(actual_df, expected_s3_df)
    
    # Crucial Verification: Check the mock was called correctly
    mock_get_object.assert_called_once_with(
        Bucket=test_bucket, 
        Key=test_key
    )
