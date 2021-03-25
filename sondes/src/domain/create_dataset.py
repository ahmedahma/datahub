import requests
from src.domain.datahub_exception import DatahubException


def create_dataset(user_name: str, dataset_name: str, file_name: str):
    api_url = f"http://localhost:8080/datasets?action=ingest"
    json = {
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

    try:
        api_response = requests.post(api_url, json=json)
    except Exception:
        raise DatahubException(f'Error connecting Datahub API ')

    if api_response.status_code != 200:
        raise DatahubException(f'Error getting API Datahub DATA ')

    return api_response.json()
