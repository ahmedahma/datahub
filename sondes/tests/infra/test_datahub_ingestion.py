import json
import os
from unittest.mock import patch

import pytest
from pydantic.error_wrappers import ValidationError
from src.infra.datahub_ingestion import _create_pipeline, send_event_and_run_ingestion

from datahub.configuration import DynamicTypedConfig
from datahub.ingestion.run.pipeline import SourceConfig


@pytest.fixture
def dataset_mce_object():
    pathname = os.path.dirname(os.path.abspath(__file__))
    filename = 'dataset_mce_fixture.json'
    dataset_mce_pathname = os.path.join(pathname, filename)
    with open(dataset_mce_pathname) as json_file:
        dataset_mce_object = json.load(json_file)
    return dataset_mce_object


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


@patch('src.infra.datahub_ingestion._run_ingestion_pipeline')
def test_send_event_and_run_ingestion_runs_successfully_given_correct_mce(mocked_run_ingestion_pipeline,
                                                                          dataset_mce_object):
    # Given
    dataset_mce_json = dataset_mce_object

    # When
    send_event_and_run_ingestion(dataset_mce_json)

    # Then
    mocked_run_ingestion_pipeline.assert_called_once()


def test_send_event_and_run_ingestion_raises_error_given_incorrect_mce():
    # Given
    fake_mce_json = {'fake_mce': 'fake_mce'}

    # When
    with pytest.raises(ValueError) as errors:
        send_event_and_run_ingestion(fake_mce_json)

    # Then
    assert str(errors.value) == f"failed to parse into valid MCE: {fake_mce_json}"
