from unittest.mock import MagicMock, patch

from infra.get_data_from_datagalaxy import get_all_sources, get_source_by_id


@patch('src.infra.get_data_from_datagalaxy.requests.get')
def test_get_all_sources_returns_request_response_from_api(request_get):
    # Given
    authorization_token = 'fake_token'
    expected_api_response = {
        "pages": 0,
        "total": 0,
        "total_sum": 0,
        "results": [
            {
                "id": "string",
                "name": "string",
                "technicalName": "string",
                "path": "string",
                "type": "string",
                "location": "string",
                "accessData": {
                    "hasOfficialRoleAttributesWriteAccess": True,
                    "hasEntityStatusWriteAccess": True,
                    "hasSuggestionModeWriteAccess": True,
                    "hasTaskWriteAccess": True,
                    "hasReadAccess": True,
                    "hasWriteAccess": True,
                    "hasAdministratorAccess": True,
                    "hasImportAccess": True,
                    "hasExportAccess": True,
                    "hasDeleteAccess": True,
                    "hasCreateAccess": True,
                    "hasManagementAccess": True
                }
            }
        ],
        "next_page": "string"
    }

    response_return_value = MagicMock(status_code=200, text='')
    response_return_value.json = MagicMock(return_value=expected_api_response)
    request_get.return_value = response_return_value

    # When
    actual_api_response = get_all_sources(authorization_token)

    # Then
    request_get.assert_called_once_with('https://total.datagalaxy.com/sources',
                                        headers={'Authorization': 'Bearer fake_token'})

    assert actual_api_response == expected_api_response


@patch('src.infra.get_data_from_datagalaxy.requests.get')
def test_get_source_by_id_returns_request_response_from_api(request_get):
    # Given
    authorization_token = 'fake_token'
    source_id = 1
    version_id = 1
    expected_api_response = {
        "name": "string",
        "technicalName": "string",
        "type": "string",
        "id": "string",
        "versionId": "string",
        "path": "string",
        "attributes": {}
    }

    response_return_value = MagicMock(status_code=200, text='')
    response_return_value.json = MagicMock(return_value=expected_api_response)
    request_get.return_value = response_return_value

    # When
    actual_api_response = get_source_by_id(authorization_token, source_id, version_id)

    # Then
    request_get.assert_called_once_with('https://total.datagalaxy.com/sources/1/1',
                                        headers={'Authorization': 'Bearer fake_token'})

    assert actual_api_response == expected_api_response

