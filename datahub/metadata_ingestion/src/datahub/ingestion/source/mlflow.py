from dataclasses import dataclass, field
from typing import Iterable, List

import mlflow.sklearn
from datahub.configuration import ConfigModel
from datahub.configuration.common import AllowDenyPattern
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.source.metadata_common import MetadataWorkUnit
from datahub.metadata import MLModelPropertiesClass
from datahub.metadata.com.linkedin.pegasus2avro.common import VersionTag
from datahub.metadata.com.linkedin.pegasus2avro.metadata.snapshot import MLModelSnapshot
from datahub.metadata.com.linkedin.pegasus2avro.mxe import MetadataChangeEvent
from mlflow.entities import ViewType


class MlFlowConfig(ConfigModel):
    tracking_uri: str

    experiment_pattern: AllowDenyPattern = AllowDenyPattern(deny=["Default"])
    path_pattern: str = 'model/model.pkl'


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
        experiments = self.get_mlflow_objects(self.mlflow_client)

        for experiment in experiments:
            if self.config.experiment_pattern.allowed(experiment.name):
                mce = MetadataChangeEvent()
                mlmodel_snapshot = MLModelSnapshot()
                mlmodel_snapshot.urn = f"urn:li:mlModel:(urn:li:dataPlatform:{platform},{experiment.name},{env})"

                mlmodel_snapshot.aspects.append(experiment)

                mce.proposedSnapshot = mlmodel_snapshot

                wu = MetadataWorkUnit(id=experiment.name, mce=mce)
                self.report.report_workunit(wu)
                yield wu
            else:
                self.report.report_dropped(experiment.name)

    def get_mlflow_objects(self, mlflow_client: mlflow.tracking.MlflowClient) -> List[MLModelPropertiesClass]:
        experiment_list = mlflow_client.list_experiments(view_type=ViewType.ACTIVE_ONLY)
        experiments_ids_list = list(map(lambda x: x.experiment_id, iter(experiment_list)))
        runs_of_experiment = mlflow_client.search_runs(experiments_ids_list)
        experiments_metadata = []

        for run in runs_of_experiment:
            experiments_metadata.append(MLModelPropertiesClass(
                name=run.data.tags['mlflow.source.name'],
                date=run.info.end_time,
                version=VersionTag({'versionTag': run.info.run_id}),
                hyperParameters=run.data.params,
                metrics=run.data.metrics
            ))

        return experiments_metadata

    def get_report(self) -> MlFlowSourceReport:
        return self.report
