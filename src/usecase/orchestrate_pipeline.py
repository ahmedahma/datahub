import numpy as np

from src.domain.transformation_pipeline import build_normalized_mes_context_table_from_mes_context
from src.infra.load_tables import load_table_from_dump_name


def construct_temporal_trace_refined_table_from_rousset_fdc_data():

    # Load Datafiles
    MES_ASSOCIATION_TABLE_METADATA = {
        'filename': 'PCB.MESFDCAssociation.dump',
        'names': ['context_id', 'mes_context_id'],
        'types': {
            'context_id': np.int64,
            'mes_context_id': np.int64,
        },
        'null_value': 'N.A.'
    }
    MES_CONTEXT_DEFINITION_TABLE_TABLE_METADATA = {
        'filename': 'PCB.MESContextHistory.dump',
        'names': ['mes_context_id', 'technology_name', 'product_name', 'lot_name', 'wafer_name',
                  'route_name', 'stage_name', 'operation_name', 'aux1', 'aux2'],
        'types': {
            'mes_context_id': np.float64,
            'technology_name': str,
            'product_name': str,
            'lot_name': str,
            'wafer_name': str,
            'route_name': str,
            'stage_name': str,
            'operation_name': str,
            'aux1': str,
            'aux2': str
        },
        'null_value': 'N.A.'
    }

    mes_context_definition_table = load_table_from_dump_name(MES_CONTEXT_DEFINITION_TABLE_TABLE_METADATA)
    mes_association_table = load_table_from_dump_name(MES_ASSOCIATION_TABLE_METADATA)
    normalized_mes_context_table = build_normalized_mes_context_table_from_mes_context(mes_context_definition_table,
                                                                                       mes_association_table)
    return normalized_mes_context_table
