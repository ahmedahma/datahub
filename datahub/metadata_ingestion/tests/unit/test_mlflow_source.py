import unittest

from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.source.mlflow import MlFlowSource
from datahub.metadata.com.linkedin.pegasus2avro.mxe import MetadataChangeEvent


class MlFlowSourceTest(unittest.TestCase):
    def test_mlflow_source_configuration(self):
        # Given:
        config = {
            'tracking_uri': 'localhost:5000',
        }

        expected_mlflow_config = config
        expected_mlflow_client_tracking_uri = config['tracking_uri']

        # When:
        ctx = PipelineContext(run_id="test")
        mlflow_source = MlFlowSource.create(config, ctx)

        actual_mlflow_config = mlflow_source.__dict__['config']
        actual_mlflow_client_tracking_uri = mlflow_source.__dict__['mlflow_client']._registry_uri

        # Then:
        assert actual_mlflow_config == expected_mlflow_config
        assert actual_mlflow_client_tracking_uri == expected_mlflow_client_tracking_uri

    def test_mlflow_source_creates_correct_workunit(self):
        # Given:
        config = {
            'tracking_uri': 'localhost:5000',
        }

        # When:
        ctx = PipelineContext(run_id="test")
        mlflow_source = MlFlowSource.create(config, ctx)

        workunits = []
        for w in mlflow_source.get_workunits():
            workunits.append(w)

        # Then:
        assert len(workunits) == 1

        workunit = workunits[0]
        assert workunit.__dict__['mce']['proposedSnapshot'][
                   'urn'] == 'urn:li:dataset:(urn:li:dataPlatform:mlflow,test_test,PROD)'

        mce = workunit.get_metadata()["mce"]
        assert isinstance(mce, MetadataChangeEvent)
