from typing import Dict

from sondes.domain.create_user import create_user
from sondes.infra.datahub_ingestion import send_event_and_run_ingestion


def ingest_user(user_model: Dict):
    user_mce_json = create_user(user_model)
    send_event_and_run_ingestion(user_mce_json)
