import os
import pickle
from dataclasses import dataclass, field
from typing import Iterable, List, Dict

import mlflow.sklearn

from datahub.configuration import ConfigModel
from datahub.configuration.common import AllowDenyPattern, OperationalError
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.source.metadata_common import MetadataWorkUnit
from datahub.metadata import MLModelPropertiesClass
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
            if not self.config.experiment_pattern.allowed(experiment['name']):
                self.report.report_dropped(experiment['name'])
                continue

            mce = MetadataChangeEvent()
            mlmodel_snapshot = MLModelSnapshot()
            mlmodel_snapshot.urn = f"urn:li:mlModel:(urn:li:dataPlatform:{platform},{experiment['name']},{env})"

            mlmodel_properties = MLModelPropertiesClass(
                tags=[],
                hyperParameters=experiment['params'],
                mlFeatures=[]
            )
            mlmodel_snapshot.aspects.append(mlmodel_properties)

            mce.proposedSnapshot = mlmodel_snapshot

            wu = MetadataWorkUnit(id=experiment['name'], mce=mce)
            self.report.report_workunit(wu)
            yield wu

    def get_mlflow_objects(self, mlflow_client: mlflow.tracking.MlflowClient) -> List[Dict]:
        experiment_list = mlflow_client.list_experiments(view_type=ViewType.ACTIVE_ONLY)
        experiments_ids_list = list(map(lambda x: x.experiment_id, iter(experiment_list)))
        runs_of_experiment = mlflow_client.search_runs(experiments_ids_list)
        experiments_metadata = []

        for run in runs_of_experiment:
            model = self.load_model_artefact(mlflow_client, run)
            experiments_metadata.append({
                'name': run.data.tags['mlflow.source.name'],
                'metrics': run.data.metrics,
                'model': model,
                'date': run.info.end_time,
                'version': run.info.experiment_id,
                'params': run.data.params
            })
        return experiments_metadata

    def load_model_artefact(self, mlflow_client, run):
        local_dir = "/tmp/artifact_downloads"
        if not os.path.exists(local_dir):
            os.mkdir(local_dir)

        model_path = mlflow_client.download_artifacts(run_id=run.info.run_id, path=self.config.path_pattern,
                                                      dst_path=local_dir)
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        return model

    def get_report(self) -> MlFlowSourceReport:
        return self.report
