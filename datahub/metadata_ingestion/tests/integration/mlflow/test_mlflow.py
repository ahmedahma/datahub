import shutil
import unittest
from typing import List

import pickle
import mlflow
import numpy as np
import pandas as pd
from datahub.ingestion.run.pipeline import Pipeline
from sklearn import datasets
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import train_test_split

from test_helpers.mce_helpers import load_json_file, assert_mces_equal


class MlFlowTest(unittest.TestCase):
    def test_mlflow_ingests_multiple_mlflow_experiments_successfully(self):
        # Given:
        tracking_uri = 'http://localhost:5000'
        mlflow_client = mlflow.tracking.MlflowClient(tracking_uri)
        name = 'heyyyyy'
        first_experiment_id = mlflow_client.create_experiment(name=name)
        mlflow.set_experiment(name)

        mlflow_client.create_run(first_experiment_id)
        model = DummyRegressor()

        diabetes = datasets.load_diabetes()
        X = diabetes.data
        y = diabetes.target

        Y = np.array([y]).transpose()
        d = np.concatenate((X, Y), axis=1)
        cols = ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6', 'progression']
        data = pd.DataFrame(d, columns=cols)

        train, test = train_test_split(data, test_size=0.2)
        train_x = train.drop(["progression"], axis=1)
        train_y = train[["progression"]]

        tags = {'model_type': 'lr_baseline'}

        with mlflow.start_run():
            model.fit(train_x, train_y)
            mlflow.log_metric("mae", 123)
            mlflow.sklearn.log_model(model, "model")
            mlflow.set_tags(tags)

        golden_mce = load_json_file(filename="./mlflow_golden_mce.json")

        recipient = {
            "source": {
                "type": "mlflow",
                "config": {
                    "tracking_uri": tracking_uri,
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

        # Then
        assert status == 0
        assert_mces_equal(output_mce, golden_mce)
