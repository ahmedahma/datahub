from infra.repository.datagalaxy_dataset_repository import DataGalaxyDatasetRepository
from usecase.ingest_dataset_in_datagalaxy import ingest_dataset_in_datagalaxy


def test_ingest_dataset_in_datagalaxy_ingests_dataset_successfully_in_datagalaxy():
    # Given
    dataset_object = {
        "name": 'test3',
        "status": 'Proposed',
        "owners": [
            "khadidia.sy@external.total.com"
        ],
        "stewards": [
            "khadidia.sy@external.total.com"
        ],
        "tags": [

        ],
        "description": 'test ingestion',
        "summary": 'Ingestion in datagalaxy',
        "upsert": True,
        "type": 'NoSql',
        "technicalName": 'test dataset'
    }
    version_id = '2f21af4f-c434-40c7-8543-98121bbb62df'

    repository = DataGalaxyDatasetRepository()

    # When
    datagalaxy_response_post = ingest_dataset_in_datagalaxy(dataset_object, version_id)
    dataset_id = datagalaxy_response_post['id']
    posted_datagalaxy_dataset = repository.get_by_id(dataset_id, version_id)

    # Then
    assert posted_datagalaxy_dataset['name'] == dataset_object['name']
    assert posted_datagalaxy_dataset['attributes']['owners'] == dataset_object['owners']
