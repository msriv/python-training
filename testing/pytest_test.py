import pytest
from .calculator import add
 
@pytest.fixture
def sample_list():
    return [1,2,3]
 
def test_add_list_of_numbers(sample_list):
    assert add(sample_list) == 6