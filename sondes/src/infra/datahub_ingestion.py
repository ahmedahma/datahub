import os
import tempfile
from typing import Dict

from src.infra.utils import _dump_mce_in_file

from datahub.ingestion.run.pipeline import Pipeline


# test send file with a persistent file
def send_event_and_run_ingestion(mce_json: Dict):
    mce_tmp_file = tempfile.NamedTemporaryFile(mode="w+", suffix='.json', delete=False)
    _dump_mce_in_file(mce_json, mce_tmp_file.name)

    pipeline_config = _create_pipeline_configuration(mce_tmp_file.name)
    run_ingestion_pipeline(pipeline_config)

    os.remove(mce_tmp_file.name)


# Envoyer un code de retour
def run_ingestion_pipeline(pipeline_config: Dict):
    pipeline = _create_pipeline(pipeline_config)
    _run_pipeline(pipeline)
    pipeline.raise_from_status()
    pipeline.pretty_print_summary()


def _run_pipeline(pipeline: Pipeline):
    pipeline.run()


def _create_pipeline(pipeline_config: Dict) -> Pipeline:
    pipeline = Pipeline.create(pipeline_config)
    return pipeline


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
            "config": {"server": "http://localhost:8080"},
        },
    }
    return pipeline_config
