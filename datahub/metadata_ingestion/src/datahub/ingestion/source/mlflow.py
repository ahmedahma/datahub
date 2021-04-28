from dataclasses import dataclass, field
from typing import Iterable, List

import mlflow.sklearn

from datahub.configuration import ConfigModel
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.source.metadata_common import MetadataWorkUnit
from datahub.metadata import DatasetPropertiesClass
from datahub.metadata.com.linkedin.pegasus2avro.metadata.snapshot import DatasetSnapshot
from datahub.metadata.com.linkedin.pegasus2avro.mxe import MetadataChangeEvent


## TODO: ALLOW_DENY_LIST
## TODO: HOST/PORT + TRACKING_URI, REGISTRY URI ?
## TODO: second type of servers

class MlFlowConfig(ConfigModel):
    tracking_uri: str


@dataclass
class MlFlowSourceReport(SourceReport):
    filtered: List[str] = field(default_factory=list)

    def report_dropped(self, name: str) -> None:
        self.filtered.append(name)


class MlFlowSource(Source):
    config: MlFlowConfig

    def __init__(self, config: MlFlowConfig, ctx: PipelineContext):
        super().__init__(ctx)
        self.config = config
        self.mlflow_client = mlflow.tracking.MlflowClient(tracking_uri=self.config.tracking_uri)
        self.report = MlFlowSourceReport()

    @classmethod
    def create(cls, config_dict: dict, ctx: PipelineContext):
        config = MlFlowConfig.parse_obj(config_dict)
        return cls(config, ctx)

    def get_workunits(self) -> Iterable[MetadataWorkUnit]:
        platform = 'mlflow'
        env = 'PROD'

        dataset_name_list = self.get_mlflow_objects(self.mlflow_client)

        for dataset_name in dataset_name_list:
            mce = MetadataChangeEvent()
            dataset_snapshot = DatasetSnapshot()
            dataset_snapshot.urn = f"urn:li:dataset:(urn:li:dataPlatform:{platform},{dataset_name},{env})"

            dataset_properties = DatasetPropertiesClass(
                tags=[],
                customProperties={},
            )
            dataset_snapshot.aspects.append(dataset_properties)

            mce.proposedSnapshot = dataset_snapshot

            wu = MetadataWorkUnit(id=dataset_name, mce=mce)
            self.report.report_workunit(wu)
            yield wu

    @staticmethod
    def get_mlflow_objects(mlflow_client: mlflow.tracking.MlflowClient) -> List[str]:
        experiment_list = mlflow_client.list_experiments()
        experiment_name_list = [experiment.name for experiment in experiment_list]
        return experiment_name_list

    def get_report(self) -> MlFlowSourceReport:
        return self.report
