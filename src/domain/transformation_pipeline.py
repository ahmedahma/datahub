import datetime

import pandas as pd


# Transformation : normalise contexts between automation and fdc systems
def build_normalized_mes_context_table_from_mes_context(mes_context_table, mes_association_table):
    normalized_mes_context = pd.merge(mes_association_table,
                                      mes_context_table,
                                      how='left')
    yearmonth = '202011'
    equipment = 'MSPO7'
    yesterday = get_yesterday_formatted_date()
    associated_mes_context = normalized_mes_context \
        .assign(equipment=lambda x: equipment) \
        .assign(yearmonth=lambda x: yearmonth) \
        .assign(loading_day=lambda x: yesterday) \
        .rename(columns={
            'product_name': 'cam_product',
            'technology_name': 'technology',
            'lot_name': 'lot_id',
            'wafer_name': 'wafer_id',
            'stage_name': 'stage',
            'operation_name': 'operation'
        })
    final_columns = ['context_id', 'loading_day', 'mes_context_id', 'technology', 'cam_product', 'lot_id',
                     'wafer_id', 'stage', 'operation', 'aux1', 'aux2', 'equipment', 'yearmonth']
    return associated_mes_context[final_columns]


# Transformation : get previous day as loading day, to change
def get_yesterday_formatted_date():
    return datetime.date.today() - datetime.timedelta(days=1)
