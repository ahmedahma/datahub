from dataclasses import dataclass, field
from typing import Iterable, List

import mlflow.sklearn

from datahub.configuration import ConfigModel
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.source.metadata_common import MetadataWorkUnit
from datahub.metadata import MLModelPropertiesClass
from datahub.metadata.com.linkedin.pegasus2avro.metadata.snapshot import MLModelSnapshot
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

        mlmodel_experiments_list = self.get_mlflow_objects(self.mlflow_client)

        for mlmodel_experiment in mlmodel_experiments_list:
            mce = MetadataChangeEvent()
            mlmodel_snapshot = MLModelSnapshot()
            mlmodel_snapshot.urn = f"urn:li:mlModel:(urn:li:dataPlatform:{platform},{mlmodel_experiment},{env})"

            mlmodel_properties = MLModelPropertiesClass(
                tags=[],
                hyperParameters={},
                mlFeatures=[]
            )
            mlmodel_snapshot.aspects.append(mlmodel_properties)

            mce.proposedSnapshot = mlmodel_snapshot

            wu = MetadataWorkUnit(id=mlmodel_experiment, mce=mce)
            self.report.report_workunit(wu)
            yield wu

    @staticmethod
    def get_mlflow_objects(mlflow_client: mlflow.tracking.MlflowClient) -> List[str]:
        experiment_list = mlflow_client.list_experiments()
        default_experiment_name = 'Default'
        experiment_name_list = [experiment.name for experiment in experiment_list if
                                experiment.name != default_experiment_name]
        return experiment_name_list

    def get_report(self) -> MlFlowSourceReport:
        return self.report
