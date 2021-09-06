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
    def get_all(self, version_id):
        return NotImplementedError


class DataGalaxyDatasetRepository(DatasetAbstractRepository):
    def __init__(self):
        self.integration_token = os.environ.get("DATAGALAXY_INTEGRATION_TOKEN", None)
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

    def get_structure_by_id(self, structure_id, version_id):
        api_url = f'https://api.datagalaxy.com/v2/structures/{version_id}/{structure_id}'
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
                print(api_response)
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
                print(api_response.json())
                raise DataGalaxyException(f'Error posting data in Datagalaxy API ')

        return api_response.json()

    def get_all(self, version_id):
        api_url = f'https://api.datagalaxy.com/v2/sources?versionId={version_id}'
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
                print(api_response.json())
                raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

        return api_response.json()

    def get_all_structures(self, version_id):
        api_url = f'https://api.datagalaxy.com/v2/structures?versionId={version_id}'
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
                print(api_response.json())
                raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

        return api_response.json()

    def add_structure(self, structure_name, parent_id, version_id):
        api_url = f'https://api.datagalaxy.com/v2/structures/{version_id}/{parent_id}'
        headers = {'Authorization': 'Bearer ' + self.access_token}
        structure = {'name': 'Test table',
                     'technicalName': structure_name,
                     'type': 'Table',
                     'displayName': structure_name,
                     'versionId': version_id,
                     'path': '\\OBJECT-1\\public\\area',
                     'typePath': '\\Relational\\Model\\Table',
                     'attributes': {'technicalName': 'area', 'description': 'Table for wellheads', 'Golden Source': [],
                                    'status': 'Proposed',
                                    'logicalParentData': {'name': 'public', 'technicalName': 'public', 'type': 'Model',
                                                          'id': parent_id,#'54bdf09d-e995-4fb1-9ae9-b67e394d104c:67eabb61-48cb-4a0d-b82a-05d09b2bfce3',
                                                          'parentList': ['ae158fab-d18c-413b-bdd4-bcd0636e4659']},
                                    'childrenCount': 4,
                                    'External ID': '', 'Data Frequency': None, 'Data Frequency Details': '',
                                    'Confidentiality level': '1', 'Contains personal data (privacy)': '1',
                                    'Non-Availability': None,
                                    'Non-Integrity': None, 'TDMG Domains': ['WELL DATA'], 'tags': ['EP'],
                                    'Data Custodian': [],
                                    'Data Owner': ['jade.leask@totalenergies.com'],
                                    'Local Data Contacts': ['jade.leask@totalenergies.com'],
                                    'owners': ['maurice.ketevi@external.totalenergies.com'],
                                    'stewards': ['maurice.ketevi@external.totalenergies.com'],
                                    'Internal / External data': '0',
                                    'Retention Policy': '', 'Monitoring requirements': '',
                                    'creationTime': '2021-07-08T15:17:51.2267134+02:00',
                                    'lastModificationTime': '2021-07-08T15:18:38.8496951+02:00'}
                     }

        try:
            api_response = requests.post(api_url, headers=headers, json=structure)
        except Exception:
            raise DataGalaxyException(f'Error connecting Datagalaxy API ')
        if api_response.status_code != 201:
            if api_response.status_code == 401:
                new_access_token = _get_access_token(self.integration_token)
                headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + new_access_token}
                api_response = requests.post(api_url, json=str, headers=headers)
            else:
                print(api_response.json())
                raise DataGalaxyException(f'Error posting data in Datagalaxy API ')

        return api_response.json()

    def add_field_to_structure(self, field_name, structure_id, version_id):
        api_url = f'https://api.datagalaxy.com/v2/fields/{version_id}/{structure_id}'
        headers = {'Authorization': 'Bearer ' + self.access_token}
        data = {
            "name": field_name,
            "type": "Column",
            "status": "Proposed",
            "owners": [
                "maurice.ketevi@external.totalenergies.com"
            ],
            "stewards": [
                "maurice.ketevi@external.totalenergies.com"
            ],
            "tags": [],
            "description": "Test field",
            "summary": "",
            "upsert": True,
            "technicalName": field_name,
            "displayName": field_name,
            "columnDataType": "VariableString",
            "property1": 'string',
            "property2": 'string'
        }
        try:
            api_response = requests.post(api_url, headers=headers, json=data)
            print(api_response)
        except Exception:
            raise DataGalaxyException(f'Error connecting Datagalaxy API ')
        if api_response.status_code != 201:
            if api_response.status_code == 401:
                new_access_token = _get_access_token(self.integration_token)
                headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + new_access_token}
                api_response = requests.post(api_url, json=str, headers=headers)
                print(api_response.json())
            else:
                print(api_response.json())
                raise DataGalaxyException(f'Error posting data in Datagalaxy API ')


def _get_access_token(integration_token):
    api_url = 'https://api.datagalaxy.com/v2/credentials'
    if not integration_token:
        raise DataGalaxyException(f'Error Datagalaxy token is None')

    headers = {'Authorization': 'Bearer ' + integration_token}
    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy token ')

    api_response_dict = api_response.json()

    return api_response_dict['accessToken']
