from typing import Dict

from src.infra.repository.datagalaxy_dataset_repository import DataGalaxyDatasetRepository


def ingest_dataset_in_datagalaxy(dataset_object: Dict, version_id: str):
    repository = DataGalaxyDatasetRepository()
    datagalaxy_response_post = repository.save_dataset(version_id, dataset_object)
    return datagalaxy_response_post
