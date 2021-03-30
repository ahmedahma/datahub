from src.infra.datahub_api import post_data_in_datahub


def browse_datasets():
    api_url = f"http://localhost:8080/datasets?action=browse"
    json = {"path": "", "start": 0, "limit": 10}
    api_response = post_data_in_datahub(api_url, json)

    return api_response.json()


