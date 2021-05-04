import abc
import os

import requests


class DataGalaxyException(Exception):
    pass


class DatasetAbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, dataset_id, version_id):
        return NotImplementedError

    @abc.abstractmethod
    def save_dataset(self, version_id, dataset_object):
        return NotImplementedError

    @abc.abstractmethod
    def get_all(self):
        return NotImplementedError


class DataGalaxyDatasetRepository(DatasetAbstractRepository):
    def __init__(self):
        self.integration_token = os.environ.get("DATAGALAXY_INTEGRATION_TOKEN",'')
        self.access_token = _get_access_token(self.integration_token)

    def get_by_id(self, dataset_id, version_id):
        api_url = f'https://api.datagalaxy.com/v2/sources/{version_id}/{dataset_id}'
        headers = {'Authorization': 'Bearer ' + self.access_token}

        try:
            api_response = requests.get(api_url, headers=headers)
        except Exception:
            raise DataGalaxyException(f'Error connecting Datagalaxy API ')
        if api_response.status_code != 200:
            if api_response.status_code == 401:
                new_access_token = _get_access_token(self.integration_token)
                headers = {'Authorization': 'Bearer ' + new_access_token}
                api_response = requests.get(api_url, headers=headers)
            else:
                raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

        return api_response.json()

    def save_dataset(self, version_id, dataset_object):
        api_url = f'https://api.datagalaxy.com/v2/sources/{version_id}'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.access_token}
        data = {
            "name": dataset_object['name'],
            "status": dataset_object['status'],
            "owners": dataset_object['owners'],
            "stewards": dataset_object['stewards'],
            "tags": dataset_object['tags'],
            "description": dataset_object['description'],
            "summary": dataset_object['summary'],
            "upsert": True,
            "type": dataset_object['type'],
            "technicalName": dataset_object['technicalName']
        }

        try:
            api_response = requests.post(api_url, headers=headers, json=data)
        except Exception:
            raise DataGalaxyException(f'Error connecting Datagalaxy API ')
        if api_response.status_code != 201:
            if api_response.status_code == 401:
                new_access_token = _get_access_token(self.integration_token)
                headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + new_access_token}
                api_response = requests.post(api_url, json=data, headers=headers)
            else:
                raise DataGalaxyException(f'Error posting data in Datagalaxy API ')

        return api_response.json()

    def get_all(self):
        api_url = 'https://api.datagalaxy.com/v2/sources'
        headers = {'Authorization': 'Bearer ' + self.access_token}

        try:
            api_response = requests.get(api_url, headers=headers)
        except Exception:
            raise DataGalaxyException(f'Error connecting Datagalaxy API ')
        if api_response.status_code != 200:
            if api_response.status_code == 498:
                new_access_token = _get_access_token(self.integration_token)
                headers = {'Authorization': 'Bearer ' + new_access_token}
                api_response = requests.get(api_url, headers=headers)
            else:
                raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

        return api_response.json()


def _get_access_token(integration_token):
    api_url = 'https://api.datagalaxy.com/v2/credentials'
    headers = {'Authorization': 'Bearer ' + integration_token}
    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy token ')

    api_response_dict = api_response.json()

    return api_response_dict['accessToken']
