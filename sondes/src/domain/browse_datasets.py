import requests
from src.domain.datahub_exception import DatahubException


def browse_datasets():
    api_url = f"http://localhost:8080/datasets?action=browse"
    json = {"path": "", "start": 0, "limit": 10}

    try:
        api_response = requests.post(api_url, json=json)
    except Exception:
        raise DatahubException(f'Error connecting Datahub API ')

    if api_response.status_code != 200:
        raise DatahubException(f'Error getting API Datahub DATA ')

    return api_response.json()
