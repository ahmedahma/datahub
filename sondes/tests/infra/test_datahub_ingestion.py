import json
import os

import pytest
from pydantic.error_wrappers import ValidationError
from src.infra.datahub_ingestion import _create_pipeline

from datahub.configuration import DynamicTypedConfig
from datahub.ingestion.run.pipeline import SourceConfig


@pytest.fixture
def dataset_mce_pathname():
    pathname = os.path.dirname(os.path.abspath(__file__))
    filename = 'dataset_mce_fixture.json'
    dataset_mce_pathname = os.path.join(pathname, filename)
    return dataset_mce_pathname


def test_create_pipeline_creates_pipeline_given_correct_configuration(dataset_mce_pathname):
    # Given
    config = {
        "source": {
            "type": "file",
            "config": {
                "filename": dataset_mce_pathname,
            },
        },
        "sink": {
            "type": "datahub-rest",
            "config": {"server": "http://localhost:8080"},
        },
    }

    expected_datahub_source_config = SourceConfig(type='file', config={
        'filename': '/Users/a.alaoui.abdallaoui/tdf_innovation/sondes/tests/infra/dataset_mce_fixture.json'})
    expected_datahub_sink_config = DynamicTypedConfig(type='datahub-rest', config={'server': 'http://localhost:8080'})

    # When
    pipeline = _create_pipeline(config)

    # Then

    actual_datahub_source_config = pipeline.__dict__['config'].source
    actual_datahub_sink_config = pipeline.__dict__['config'].sink

    assert actual_datahub_source_config == expected_datahub_source_config
    assert actual_datahub_sink_config == expected_datahub_sink_config


def test_create_pipeline_raises_error_given_incorrect_configuration(dataset_mce_pathname):
    # Given
    config = {
        "sink": {
            "type": "datahub-rest",
            "config": {"server": "http://localhost:8080"},
        }
    }

    # When
    with pytest.raises(ValidationError) as errors:
        _create_pipeline(config)

    # Then
    assert 'field required', 'validation error' in str(errors.value)
