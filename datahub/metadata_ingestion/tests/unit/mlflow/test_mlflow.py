import os
import unittest

import mlflow

from datahub.ingestion.run.pipeline import Pipeline
from tests.test_helpers.mce_helpers import load_json_file, assert_mces_equal

#TODO: refacto


def load_mce(filename: str):
    pathname = os.path.dirname(os.path.abspath(__file__))
    mce_pathname = os.path.join(pathname, filename)
    mce = load_json_file(mce_pathname)
    return mce


class MlFlowTest(unittest.TestCase):
    def test_mlflow_ingest_one_experiment_from_hardcoded_configuration(self):
        # Given:
        mlflow_client = mlflow.tracking.MlflowClient(tracking_uri='localhost:5000')
        first_experiment_id = mlflow_client.create_experiment(name='first_experiment')
        second_experiment_id = mlflow_client.create_experiment(name='second_experiment')

        golden_mce = load_mce(filename="mlflow_golden_mce.json")

        recipient = {
            "source": {
                "type": "mlflow",
                "config": {
                    "tracking_uri": "localhost:5000"
                },
            },
            "sink": {
                "type": "file",
                "config": {
                    "filename": "./mlflow_mce.json"
                }
            },
        }

        pipeline = Pipeline.create(recipient)

        # When:
        pipeline.run()
        pipeline.raise_from_status()
        status = pipeline.pretty_print_summary()

        mlflow_client.delete_experiment(first_experiment_id)
        mlflow_client.delete_experiment(second_experiment_id)

        output_mce = load_mce(filename="mlflow_mce.json")


        # Then
        assert status == 0
        assert_mces_equal(output_mce, golden_mce)
