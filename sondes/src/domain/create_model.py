from typing import List


def create_model(mlmodel_model):
    model_json = {
        "auditHeader": None,
        "proposedSnapshot": {
            "com.linkedin.pegasus2avro.metadata.snapshot.DatasetSnapshot": {
                "urn": f"urn:li:dataset:(urn:li:dataPlatform:machine_learning_demo,{mlmodel_model['dataplatform_name']},PROD)",
                "aspects": [
                    {
                        "com.linkedin.pegasus2avro.schema.SchemaMetadata": {
                            "schemaName": "machine_learning",
                            "platform": f"urn:li:dataPlatform:{mlmodel_model['dataplatform_name']}",
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

    model_json['proposedSnapshot']['com.linkedin.pegasus2avro.metadata.snapshot.DatasetSnapshot']['aspects'][0][
        'com.linkedin.pegasus2avro.schema.SchemaMetadata']['fields'] = _format_dataset_fields_list(mlmodel_model['fields'])

    return model_json


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
                    "com.linkedin.pegasus2avro.schema.IntegerType": {}
                }
            },
            "nativeDataType": 'integer'
        }
        dataset_fields_list.append(field_dict)

    return dataset_fields_list