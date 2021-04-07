import os
import pandas as pd

INITIAL_TARGET_NA_VALUES = "\\N"

FDC_DUMP_DELIMITER = " "


def load_table_from_dump_name(METADATA):
    """Load table from fdc dataset providing exact dump file name & header"""

    pathname = os.path.dirname(os.path.abspath(__file__))
    filename = METADATA['filename']
    NULL_VALUE = INITIAL_TARGET_NA_VALUES
    dates_columns = False
    if 'null_value' in METADATA:
        NULL_VALUE = METADATA['null_value']
    if 'dates' in METADATA:
        dates_columns = METADATA['dates']
    table_relative_path = os.path.join("data/sequence_description_extract/PCB@MSP07@2020-11-08~20-36-16.764/",
                                       filename)
    table_path_name = os.path.join(pathname, table_relative_path)
    df_table = pd.read_csv(table_path_name,
                           delimiter=",",
                           names=METADATA['names'],
                           dtype= METADATA['types'],
                           na_values=NULL_VALUE,
                           index_col=False,
                           parse_dates=dates_columns)
    return df_table
