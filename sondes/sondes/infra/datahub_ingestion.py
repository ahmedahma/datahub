import json
import os
from typing import Dict

from datahub.ingestion.run.pipeline import Pipeline

DATAHUB_HOST = 'localhost'
DATAHUB_PORT = '8080'


def send_event_and_run_ingestion(mce_json: Dict):
    mce_file_pathname = _build_mce_file_pathname()
    _dump_mce_in_file(mce_json, mce_file_pathname)

    pipeline_config = _create_pipeline_configuration(mce_file_pathname)
    ingestion_status_code = _run_ingestion_pipeline(pipeline_config)

    os.remove(mce_file_pathname)

    return ingestion_status_code


def _build_mce_file_pathname() -> str:
    pathname = os.path.dirname(os.path.abspath(__file__))
    filename = 'mce.json'
    mce_file_pathname = os.path.join(pathname, filename)
    return mce_file_pathname


def _dump_mce_in_file(mce_json: Dict, mce_file_path: str):
    with open(mce_file_path, 'w') as file:
        json.dump(mce_json, file)


def _run_ingestion_pipeline(pipeline_config: Dict):
    pipeline = _create_pipeline(pipeline_config)
    _run_pipeline(pipeline)
    pipeline.raise_from_status()
    pipeline_summary = pipeline.pretty_print_summary()
    return pipeline_summary


def _run_pipeline(pipeline: Pipeline):
    pipeline.run()


def _create_pipeline(pipeline_config: Dict) -> Pipeline:
    pipeline = Pipeline.create(pipeline_config)
    return pipeline


# localhost !!?
def _create_pipeline_configuration(mce_file_pathname: str) -> Dict:
    pipeline_config = {
        "source": {
            "type": "file",
            "config": {
                "filename": mce_file_pathname,
            },
        },
        "sink": {
            "type": "datahub-rest",
            "config": {
                "server": f"http://{DATAHUB_HOST}:{DATAHUB_PORT}"
            }
        },
    }
    return pipeline_config
