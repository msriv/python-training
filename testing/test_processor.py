import pandas as pd
from .data_processor import capitalize_column
from pandas.testing import assert_frame_equal
 
def test_capitalize_column_correctly():
    # ARRANGE
    input_data = {
        'ID': [1,2,3],
        'Name': ['vishwas','jagan','puri'],
        'Values': [10,20,30]
    }
 
    input_df = pd.DataFrame(input_data)
 
    expected_data = {
        'ID': [1,2,3],
        'Name': ['VISHWAS','JAGAN','PURI'],
        'Values': [10,20,30]
    }
 
    expected_df = pd.DataFrame(expected_data)
 
    # ACT
    actual_df = capitalize_column(input_df,'Name')
 
    # ASSERT
    assert_frame_equal(actual_df, expected_df)


def test_capitalize_column_non_string_column():
    # ARRANGE - test that numeric columns remain unchanged
    input_data = {
        'ID': [1, 2, 3],
        'Name': ['alice', 'bob', 'charlie'],
        'Values': [10, 20, 30]
    }
    
    input_df = pd.DataFrame(input_data)
    
    expected_data = {
        'ID': [1, 2, 3],
        'Name': ['alice', 'bob', 'charlie'],
        'Values': [10, 20, 30]
    }
    
    expected_df = pd.DataFrame(expected_data)
    
    # ACT - capitalize a numeric column (should have no effect)
    actual_df = capitalize_column(input_df, 'Values')
    
    # ASSERT
    assert_frame_equal(actual_df, expected_df)


def test_capitalize_column_empty_dataframe():
    # ARRANGE - test with empty dataframe
    input_data = {
        'ID': [],
        'Name': [],
        'Values': []
    }
    
    input_df = pd.DataFrame(input_data)
    
    expected_data = {
        'ID': [],
        'Name': [],
        'Values': []
    }
    
    expected_df = pd.DataFrame(expected_data)
    
    # ACT
    actual_df = capitalize_column(input_df, 'Name')
    
    # ASSERT
    assert_frame_equal(actual_df, expected_df)