from typing import Dict, List


def create_dataset(dataset_model: Dict) -> Dict:
    dataset_json = {
        "auditHeader": None,
        "proposedSnapshot": {
            "com.linkedin.pegasus2avro.metadata.snapshot.DatasetSnapshot": {
                "urn": f"urn:li:dataset:(urn:li:dataPlatform:{dataset_model['dataplatform_name']},"
                f"{dataset_model['dataset_name']},PROD)",
                "aspects": [
                    {
                        "com.linkedin.pegasus2avro.schema.SchemaMetadata": {
                            "schemaName": f"{dataset_model['dataset_name']}",
                            "platform": f"urn:li:dataPlatform:{dataset_model['dataplatform_name']}",
                            "version": 0,
                            "created": {
                                "time": 1581407189000,
                                "actor": ""
                            },
                            "lastModified": {
                                "time": 1581407189000,
                                "actor": ""
                            },
                            "hash": "",
                            "platformSchema": {
                                "com.linkedin.pegasus2avro.schema.KafkaSchema": {
                                    "documentSchema": ""
                                }
                            }
                        }
                    }
                ]
            }
        },
        "proposedDelta": None
    }

    dataset_json['proposedSnapshot']['com.linkedin.pegasus2avro.metadata.snapshot.DatasetSnapshot']['aspects'][0][
        'com.linkedin.pegasus2avro.schema.SchemaMetadata']['fields'] = _format_dataset_fields_list(dataset_model['fields'])

    return dataset_json


def _format_dataset_fields_list(dataset_fields: List) -> List:
    dataset_fields_list = []
    for field in dataset_fields:
        field_dict = {
            "fieldPath": field['name'],
            "description": {
                "string": field['description']
            },
            "type": {
                "type": {
                    f"com.linkedin.pegasus2avro.schema.{field['pegasus_type']}": {}
                }
            },
            "nativeDataType": field['type']
        }
        dataset_fields_list.append(field_dict)

    return dataset_fields_list
