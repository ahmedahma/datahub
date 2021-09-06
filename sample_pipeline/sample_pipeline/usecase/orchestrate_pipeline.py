from click._compat import raw_input
from sondes.infra.repository.datagalaxy_dataset_repository import DataGalaxyDatasetRepository

from sondes.usecase.ingest_dataset import ingest_dataset
from sondes.usecase.ingest_dataset_in_datagalaxy import ingest_dataset_in_datagalaxy


def construct_temporal_trace_refined_table_from_rousset_fdc_data():
    repository = DataGalaxyDatasetRepository()
    version_id = '2f21af4f-c434-40c7-8543-98121bbb62df'

    datahub_object = {
        'dataplatform_name': 'tdf_demo_folder_2',
        'dataset_name': 'tdf_demo_pipeline_2',
        'fields': [
            {
                # DATASET COLUMN
                'name': 'context_id',
                'type': 'integer',
                'pegasus_type': 'IntegerType',
                'description': 'hello id'
            },
            {
                # DATASET COLUMN
                'name': 'mes_context_id',
                'type': 'integer',
                'pegasus_type': 'IntegerType',
                'description': 'second id'
            }
        ]
    }

    # Publication initiale dans DataGalaxy
    datagalaxy_relational_object = {
        "name": 'relational_object',
        "status": 'Proposed',
        "owners": [
            "khadidia.sy@external.totalenergies.com"
        ],
        "stewards": [
            "khadidia.sy@external.totalenergies.com"
        ],
        "tags": [

        ],
        "description": 'tdf demo pipeline 2',
        "summary": 'Ingestion in datagalaxy of a relational object',
        "upsert": True,
        "type": 'Relational',
        "technicalName": 'relational_object'
    }

    datagalaxy_nosql_object = {
        "name": 'nosql_object',
        "status": 'Proposed',
        "owners": [
            "khadidia.sy@external.totalenergies.com"
        ],
        "stewards": [
            "khadidia.sy@external.totalenergies.com"
        ],
        "tags": [

        ],
        "description": 'Tdf demo pipeline 2',
        "summary": 'Ingestion in datagalaxy of a nosql object',
        "upsert": True,
        "type": 'NoSql',
        "technicalName": 'nosql_object'
    }

    structure_name = 'demo_table'
    field_name = 'test_field'

    # Création des 2 objets
    #relational_datagalaxy_response_post = ingest_dataset_in_datagalaxy(datagalaxy_relational_object, version_id)
    #relational_dataset_id = relational_datagalaxy_response_post['id']
    #print(relational_dataset_id)
    structure = repository.add_structure(structure_name, relational_dataset_id, version_id)

    #ingest_dataset_in_datagalaxy(datagalaxy_nosql_object, version_id)


    print("Waiting confirmation to update field")
    #raw_input()
    print("Update confirmed: adding " + field_name)

    # Mise à jour de la table déclarée avec un nouveau champ à déclarer
    structure_id = '54bdf09d-e995-4fb1-9ae9-b67e394d104c:88c6de70-16b9-4621-8c65-b414e9a3735f' # structure['id']
    # structure_id = structure['id']
    field = repository.add_field_to_structure(field_name, structure_id, version_id)
    print(field)

    if field:
        print('-------------------------------')
        print('-------------------------------')
        print(field)
        print('-------------------------------')
        print('-------------------------------')
        print("Update to datagalaxy successful")
        print('-------------------------------')
        print('-------------------------------')


construct_temporal_trace_refined_table_from_rousset_fdc_data()
