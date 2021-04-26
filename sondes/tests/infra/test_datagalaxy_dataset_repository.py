from unittest.mock import patch, MagicMock

import pytest
from infra.repository.datagalaxy_dataset_repository import DataGalaxyDatasetRepository, DataGalaxyException


class TestGetById:
    @patch('src.infra.repository.datagalaxy_dataset_repository.requests.get')
    def test_get_by_id_returns_request_response_from_api(self, request_get):
        # Given
        repository = DataGalaxyDatasetRepository()
        access_token = 'fake_token'
        dataset_id = 1
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
        actual_api_response = repository.get_by_id(access_token, dataset_id, version_id)

        # Then
        request_get.assert_called_once_with('https://api.datagalaxy.com/v2/sources/1/1',
                                            headers={'Authorization': 'Bearer fake_token'})

        assert actual_api_response == expected_api_response

    @patch('src.infra.repository.datagalaxy_dataset_repository.requests.get', side_effect=Exception)
    def test_get_by_id_raises_exception_when_api_call_fails_with_connection_error(self, request_get):
        # Given
        repository = DataGalaxyDatasetRepository()
        access_token = 'fake_token'
        dataset_id = 1
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
        with pytest.raises(DataGalaxyException) as datagalaxy_exception:
            repository.get_by_id(access_token, dataset_id, version_id)

        # Then
        assert str(datagalaxy_exception.value) == "Error connecting Datagalaxy API "


class TestSaveDataset:
    @patch('src.infra.repository.datagalaxy_dataset_repository.requests.post')
    def test_save_dataset_posts_source_in_datagalaxy_api(self, request_post):
        # Given
        repository = DataGalaxyDatasetRepository()
        access_token = 'fake_token'
        source_object = {
            "name": 'test',
            "status": 'Proposed',
            "owners": [
                'DUC'
            ],
            "stewards": [
                'b2o'
            ],
            "tags": [
                'élie'
            ],
            "description": 'test ingestion',
            "summary": 'Ingestion in datagalaxy',
            "upsert": True,
            "type": 'dataset',
            "technicalName": 'test dataset'
        }
        version_id = 1

        expected_api_response = {
            "id": f'{version_id}',
            "location": "folder/test"
        }

        response_return_value = MagicMock(status_code=200, text='')
        response_return_value.json = MagicMock(return_value=expected_api_response)
        request_post.return_value = response_return_value

        # When
        actual_api_response = repository.save_dataset(access_token, version_id, source_object)

        # Then
        request_post.assert_called_once_with(f'https://api.datagalaxy.com/v2/sources/{version_id}',
                                             headers={'Authorization': 'Bearer fake_token'},
                                             data=source_object)

        assert actual_api_response == expected_api_response

    @patch('src.infra.repository.datagalaxy_dataset_repository.requests.post', side_effect=Exception)
    def test_save_dataset_raises_exception_when_api_call_fails_with_connection_error(self, request_post):
        # Given
        repository = DataGalaxyDatasetRepository()
        access_token = 'fake_token'
        source_object = {
            "name": 'test',
            "status": 'Proposed',
            "owners": [
                'DUC'
            ],
            "stewards": [
                'b2o'
            ],
            "tags": [
                'élie'
            ],
            "description": 'test ingestion',
            "summary": 'Ingestion in datagalaxy',
            "upsert": True,
            "type": 'dataset',
            "technicalName": 'test dataset'
        }
        version_id = 1

        # When
        with pytest.raises(DataGalaxyException) as datagalaxy_exception:
            repository.save_dataset(access_token, version_id, source_object)

        # Then
        assert str(datagalaxy_exception.value) == "Error connecting Datagalaxy API "


class TestGetAll:
    @patch('src.infra.repository.datagalaxy_dataset_repository.requests.get')
    def test_get_all_sources_returns_request_response_from_api(self, request_get):
        # Given
        repository = DataGalaxyDatasetRepository()
        access_token = 'fake_token'
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
        actual_api_response = repository.get_all(access_token)

        # Then
        request_get.assert_called_once_with('https://api.datagalaxy.com/v2/sources',
                                            headers={'Authorization': 'Bearer fake_token'})

        assert actual_api_response == expected_api_response


class TestGetAccessToken:
    @patch('src.infra.repository.datagalaxy_dataset_repository.requests.get')
    def test_get_access_token_returns_correct_access_token_from_integration_token(self, request_get):
        # Given
        repository = DataGalaxyDatasetRepository()
        integration_token = 'fake_integration_token'
        expected_api_response = {
            'accessToken': 'fake_access_token'
        }
        expected_access_token = expected_api_response['accessToken']

        response_return_value = MagicMock(status_code=200, text='')
        response_return_value.json = MagicMock(return_value=expected_api_response)
        request_get.return_value = response_return_value

        # When
        actual_access_token = repository._get_access_token(integration_token)

        # Then
        request_get.assert_called_once_with('https://api.datagalaxy.com/v2/credentials',
                                            headers={'Authorization': 'Bearer fake_integration_token'})

        assert actual_access_token == expected_access_token

    @patch('src.infra.repository.datagalaxy_dataset_repository.requests.get')
    def test_get_access_token_raises_exception_when_api_doesnt_return_access_token(self, request_get):
        # Given
        repository = DataGalaxyDatasetRepository()
        integration_token = 'fake_integration_token'

        response_return_value = MagicMock(status_code=403, text='')
        request_get.return_value = response_return_value

        # When

        with pytest.raises(DataGalaxyException) as datagalaxy_exception:
            repository._get_access_token(integration_token)

        # Then
        assert str(datagalaxy_exception.value) == "Error getting API Datagalaxy token "
