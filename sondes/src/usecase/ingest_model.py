from typing import Dict

from src.domain.create_model import create_model
from src.infra.datahub_ingestion import send_event_and_run_ingestion


def ingest_model(mlmodel_model: Dict):
    mlmodel_mce_json = create_model(mlmodel_model)
    send_event_and_run_ingestion(mlmodel_mce_json)
