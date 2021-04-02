from typing import Dict

from src.domain.create_dataset import create_dataset
from src.infra.datahub_ingestion import send_event_to_datahub


def ingest_dataset(dataset_model: Dict):
    dataset_mce_json = create_dataset(dataset_model)
    send_event_to_datahub(dataset_mce_json)
