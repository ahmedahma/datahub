from typing import Dict
import requests


class DataGalaxyException(Exception):
    pass


def get_all_sources(authorization_token: str) -> Dict:
    api_url = 'https://total.datagalaxy.com/sources'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()


def get_source_by_id(authorization_token: str, source_id: int, version_id: int) -> Dict:
    api_url = f'https://total.datagalaxy.com/sources/{version_id}/{source_id}'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()


def get_all_containers(authorization_token: str) -> Dict:
    api_url = 'https://total.datagalaxy.com/containers'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()


def get_container_by_id(authorization_token: str, container_id: int, version_id: int) -> Dict:
    api_url = f'https://total.datagalaxy.com/containers/{version_id}/{container_id}'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()


def get_all_structures(authorization_token: str) -> Dict:
    api_url = 'https://total.datagalaxy.com/structures'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()


def get_structure_by_id(authorization_token: str, container_id: int, version_id: int) -> Dict:
    api_url = f'https://total.datagalaxy.com/containers/{version_id}/{container_id}'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()


def get_all_properties(authorization_token: str) -> Dict:
    api_url = 'https://total.datagalaxy.com/properties'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()


def get_property_by_id(authorization_token: str, property_id: int, version_id: int) -> Dict:
    api_url = f'https://total.datagalaxy.com/properties/{version_id}/{property_id}'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()


def get_link_by_id(authorization_token: str, from_id: int, version_id: int) -> Dict:
    api_url = f'https://total.datagalaxy.com/properties/{version_id}/{from_id}'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()


def get_all_users(authorization_token: str) -> Dict:
    api_url = 'https://total.datagalaxy.com/users'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()


def get_all_workspaces(authorization_token: str) -> Dict:
    api_url = 'https://total.datagalaxy.com/workspaces'
    headers = {'Authorization': 'Bearer ' + authorization_token}

    try:
        api_response = requests.get(api_url, headers=headers)
    except Exception:
        raise DataGalaxyException(f'Error connecting Datagalaxy API ')
    if api_response.status_code != 200:
        raise DataGalaxyException(f'Error getting API Datagalaxy DATA ')

    return api_response.json()