import pandas as pd
from pandas.testing import assert_frame_equal

from deduplicate.drop_duplicate import drop_duplicate


def test_drop_duplicate_functions_correctly_drop_duplicate():
    # Given
    original_dataset = pd.DataFrame(data=[['michaela', 'neumann', '18'],
                                          ['charles', 'green', '24'],
                                          ['vanessa', 'parr', '29'],
                                          ['edward', 'denholm', '32']],
                                    index=['org_1', 'org_2', 'org_3', 'org_4'],
                                    columns=['given_name', 'surname', 'age'])

    idx = pd.MultiIndex.from_arrays([['org_1', 'org_1', 'org_3'], ['dup_1', 'dup_1_bis', 'dup_3']])

    expected_result = pd.DataFrame(data=[['michaela', 'neumann', '18'],
                                         ['vanessa', 'parr', '29']],
                                   index=['org_1', 'org_3'],
                                   columns=['given_name', 'surname', 'age'])

    # When

    actual_result = drop_duplicate(original_dataset, idx)

    # Then
    assert_frame_equal(expected_result, actual_result)
