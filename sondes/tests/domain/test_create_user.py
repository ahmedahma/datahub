import json
import os

import pytest
from sondes.domain.create_user import create_user


@pytest.fixture
def user_mce():
    pathname = os.path.dirname(os.path.abspath(__file__))
    filename = 'user_mce_fixture.json'
    user_mce_pathname = os.path.join(pathname, filename)
    with open(user_mce_pathname) as json_file:
        user_mce_object = json.load(json_file)
    return user_mce_object


def test_create_user(user_mce):
    # Given
    user_model = {
        'first_name': 'Jean Claude',
        'last_name': 'Van Damme',
        'departmentId': 'EP'
    }

    expected_mce = user_mce

    # When
    actual_user_mce_json = create_user(user_model)

    # Then
    assert actual_user_mce_json == expected_mce

