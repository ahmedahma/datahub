import shutil
import unittest
from typing import List

import mlflow
from datahub.ingestion.run.pipeline import Pipeline

from test_helpers.mce_helpers import load_json_file, assert_mces_equal


class MlFlowTest(unittest.TestCase):
    def test_mlflow_ingests_multiple_mlflow_experiments_successfully(self):
        # Given:
        tracking_uri = 'http://localhost:5000'
        mlflow_client = mlflow.tracking.MlflowClient(tracking_uri)
        first_experiment_id = mlflow_client.create_experiment(name='test')
        mlflow_client.create_run(first_experiment_id)
        mlflow.log_metric("mae", 123)

        golden_mce = load_json_file(filename="./mlflow_golden_mce.json")

        recipient = {
            "source": {
                "type": "mlflow",
                "config": {
                    "tracking_uri": tracking_uri,
                    "experiment_pattern": {
                        "deny": ['*'],
                        "allow": ['test']
                    }
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
        output_mce = load_json_file(filename="./mlflow_mce.json")

        mlflow_client.delete_experiment(first_experiment_id)
        mlflow_client.delete_experiment(second_experiment_id)

        # Then
        assert status == 0
        assert_mces_equal(output_mce, golden_mce)
