import os
import tempfile
from typing import Dict

from src.infra.dump_mce_in_file import dump_mce_in_file
from src.infra.dump_recipe_in_file import dump_recipe_in_file

from datahub.ingestion.run.pipeline import Pipeline


# Any change ( columns , users ... ) -> send all infos in mce


def send_event_to_datahub(mce_json: Dict):
    mce_tmp_file = tempfile.NamedTemporaryFile(mode="w+", suffix='.json', delete=False)
    dump_mce_in_file(mce_json, mce_tmp_file.name)

    recipe_json = {
        "source": {
            "type": "file",
            "config": {
                "filename": mce_tmp_file.name,
            },
        },
        "sink": {
            "type": "datahub-rest",
            "config": {"server": "http://localhost:8080"},
        },
    }

    recipe_tmp_file = tempfile.NamedTemporaryFile(mode="w+", suffix='.yml')
    pipeline_config = dump_recipe_in_file(recipe_json, recipe_tmp_file)

    create_ingestion_pipeline(pipeline_config)

    os.remove(mce_tmp_file.name)


def create_ingestion_pipeline(pipeline_config):
    pipeline = Pipeline.create(pipeline_config)
    pipeline.run()
    pipeline.raise_from_status()
    pipeline.pretty_print_summary()

