import json
import os

import pytest
from src.infra.datahub_ingestion import send_event_and_run_ingestion


@pytest.fixture
def dataset_mce_object():
    pathname = os.path.dirname(os.path.abspath(__file__))
    filename = 'dataset_mce_fixture.json'
    dataset_mce_pathname = os.path.join(pathname, filename)
    with open(dataset_mce_pathname) as json_file:
        dataset_mce_object = json.load(json_file)
    return dataset_mce_object


def test_ingest_data_in_datahub_ingests_dataset_succefully_given_correct_dataset_mce(dataset_mce_object, capsys):
    # Given
    dataset_mce_json = dataset_mce_object

    # When
    send_event_and_run_ingestion(dataset_mce_json)

    # Then
    captured = capsys.readouterr()

    assert 'Pipeline finished successfully' in captured.out


def test_ingest_data_in_datahub_fails_when_mce_is_not_in_correct_format(capsys):
    # Given
    fake_dataset_mce = {'fake': 'fake'}

    # When
    with pytest.raises(ValueError) as errors:
        send_event_and_run_ingestion(fake_dataset_mce)

    # Then

    captured = capsys.readouterr()

    assert str(errors.value) == f'failed to parse into valid MCE: {fake_dataset_mce}'
    assert 'Pipeline finished successfully' not in captured.out