import pyslet as pyslet
import requests
from src.domain.datahub_exception import DatahubException
import urllib.parse

def upsert_dataset_column():
    pass


def get_dataset_schema():
    api_url = f"http://localhost:8080/datasets?"

    encoded_url = urllib.parse.urlencode(f"urn:li:dataPlatform:foo")
    print(type(encoded_url))
    params = {"name": "samplekafkadataset", "origin": "PROD", "platform": encoded_url}
    headers = {'X-RestLi-Protocol-Version': '2.0.0', 'X-RestLi-Method': 'get'}
    try:
        api_response = requests.get(api_url, params=params, headers=headers)
        print(api_response.content)
    except Exception:
        raise DatahubException(f'Error connecting Datahub API ')

    if api_response.status_code != 200:
        print(api_response.text)
        raise DatahubException(f'Error getting API Datahub DATA ')

    return api_response.json()

get_dataset_schema()