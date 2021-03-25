from unittest.mock import patch, MagicMock

from src.domain.browse_datasets import browse_datasets
from src.domain.create_dataset import create_dataset


@patch('src.domain.browse_datasets.requests.post')
def test_browse_datasets_returns_correct_list_of_datasets(request_post):
    # Given
    expected_json = {
        "value": {
            "numEntities": 0,
            "pageSize": 0,
            "metadata": {
                "totalNumEntities": 1,
                "groups": [
                    {
                        "name": "prod",
                        "count": 5
                    }
                ],
                "path": ""
            },
            "from": 0,
            "entities": []
        }
    }
    response_return_value = MagicMock(status_code=200, text='')
    response_return_value.json = MagicMock(return_value=expected_json)
    request_post.return_value = response_return_value

    # When
    actual_json = browse_datasets()

    # Then
    request_post.assert_called_once_with("http://localhost:8080/datasets?action=browse",
                                         json={'path': '', 'start': 0, 'limit': 10})
    assert actual_json == expected_json


@patch('src.domain.create_dataset.requests.post')
def test_create_dataset_column_returns_correct_informations_to_upload_in_datahub(request_post):
    # Given
    user_name = 'toto'
    dataset_name = 'dataset_test'
    file_name = 'file_test'

    expected_json = {
        "snapshot": {
            "aspects": [
                {
                    "com.linkedin.common.Ownership": {
                        "owners": [
                            {
                                "owner": f"urn:li:corpuser:{user_name}",
                                "type": "DATAOWNER"
                            }
                        ],
                        "lastModified": {
                            "time": 0,
                            "actor": f"urn:li:corpuser:{user_name}"
                        }
                    }
                }
            ],
            "urn": f"urn:li:dataset:(urn:li:dataPlatform:{dataset_name},{file_name},PROD)"
        }
    }

    response_return_value = MagicMock(status_code=200, text='')
    response_return_value.json = MagicMock(return_value=expected_json)
    request_post.return_value = response_return_value

    # When
    actual_json = create_dataset(user_name, dataset_name, file_name)

    # Then
    assert actual_json == expected_json
