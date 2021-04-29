import unittest

import mlflow

from datahub.ingestion.run.pipeline import Pipeline
from tests.test_helpers.mce_helpers import load_json_file, assert_mces_equal


#TODO: refacto : delete experiments + move file to integration tests


class MlFlowTest(unittest.TestCase):
    def test_mlflow_ingests_multiple_mlflow_experiments_successfully(self):
        # Given:
        mlflow_client = mlflow.tracking.MlflowClient(tracking_uri='localhost:5000')
        first_experiment_id = mlflow_client.create_experiment(name='first_experiment')
        second_experiment_id = mlflow_client.create_experiment(name='second_experiment')

        golden_mce = load_json_file(filename="./mlflow_golden_mce.json")

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

        output_mce = load_json_file(filename="./mlflow_mce.json")

        # Then
        assert status == 0
        assert_mces_equal(output_mce, golden_mce)
