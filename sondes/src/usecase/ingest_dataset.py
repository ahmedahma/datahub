from typing import Dict

from src.domain.create_dataset import create_dataset
from src.infra.datahub_ingestion import send_event_and_run_ingestion


def ingest_dataset(dataset_model: Dict):
    dataset_mce_json = create_dataset(dataset_model)
    send_event_and_run_ingestion(dataset_mce_json)
