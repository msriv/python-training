import pytest
from unittest import mock
import pandas as pd
from pandas.testing import assert_frame_equal
from data_api import fetch_user_data

@mock.patch('data_api.requests.get')
def test_fetch_user_data_success(mock_get):
    """Tests the function when the API call succeeds."""
    
    # 1. ARRANGE: Define the Mock's behavior
    # Create a mock Response object
    mock_response = mock.Mock()
    
    # Configure the mock Response object's methods and attributes
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'status': 'success',
        'user_info': {'id': 101, 'name': 'Mock User', 'status': 'Active'}
    }
    
    # Tell the mock_get (which replaced requests.get) to return our mock_response
    mock_get.return_value = mock_response
    
    # Define the expected output DataFrame
    expected_df = pd.DataFrame([{'id': 101, 'name': 'Mock User', 'status': 'Active'}])

    # 2. ACT: Call the function
    actual_df = fetch_user_data(user_id=101)
    
    # 3. ASSERT: Verification
    # Check that the data processing logic is correct
    assert_frame_equal(actual_df, expected_df)
    
    # *** Mocking Verification (Crucial Step) ***
    # Check that requests.get was called exactly once with the correct URL
    mock_get.assert_called_once_with('http://api.externaldata.com/users/101')