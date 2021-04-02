from typing import Dict

from src.domain.create_user import create_user
from src.infra.datahub_ingestion import send_event_to_datahub


def ingest_user(user_model: Dict):
    user_mce_json = create_user(user_model)
    send_event_to_datahub(user_mce_json)
