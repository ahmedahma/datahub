import json
import os

import pytest
from src.domain.create_dataset import create_dataset


@pytest.fixture
def dataset_mce():
    pathname = os.path.dirname(os.path.abspath(__file__))
    filename = 'dataset_mce_fixture.json'
    dataset_mce_pathname = os.path.join(pathname, filename)
    with open(dataset_mce_pathname) as json_file:
        dataset_mce_object = json.load(json_file)
    return dataset_mce_object


def test_create_dataset(dataset_mce):
    # Given
    dataset_model = {
        'dataplatform_name': 'dataplatform',
        'dataset_name': 'dataset',
        'fields': [
            {
                'name': 'field1',
                'type': 'string',
                'pegasus_type': 'StringType',
                'description': 'first field'
            },
            {
                'name': 'field2',
                'type': 'boolean',
                'pegasus_type': 'BooleanType',
                'description': 'second field'
            }
        ]
    }

    expected_mce = dataset_mce

    # When
    actual_dataset_mce_json = create_dataset(dataset_model)

    # Then
    assert actual_dataset_mce_json == expected_mce
