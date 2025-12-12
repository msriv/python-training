import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from data_api import fetch_user_data

# The mocker fixture is automatically provided by the pytest-mock plugin
def test_fetch_user_data_with_mocker(mocker):
    """Tests the function using the cleaner pytest-mock syntax."""
    
    # 1. ARRANGE: Define the Mock's behavior
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'status': 'success',
        'user_info': {'id': 202, 'name': 'Pytest Mock', 'status': 'Inactive'}
    }
    
    # Use mocker.patch to replace the real function
    # mocker.patch returns the created mock object
    mock_get = mocker.patch('data_api.requests.get', return_value=mock_response)
    
    expected_df = pd.DataFrame([{'id': 202, 'name': 'Pytest Mock', 'status': 'Inactive'}])

    # 2. ACT
    actual_df = fetch_user_data(user_id=202)
    
    # 3. ASSERT
    assert_frame_equal(actual_df, expected_df)
    mock_get.assert_called_once_with('http://api.externaldata.com/users/202')