import pandas as pd
from pandas.testing import assert_frame_equal

from deduplicate.evaluation import select_candidates_from_false_prediction

original_dataset = pd.DataFrame(data=[['michaela', 'neumann', '18'],
                                      ['charles', 'green', '24'],
                                      ['vanessa', 'parr', '29'],
                                      ['edward', 'denholm', '32']],
                                index=['org_1', 'org_2', 'org_3', 'org_4'],
                                columns=['given_name', 'surname', 'age'])

duplicate_dataset = pd.DataFrame(data=[['michaela', 'neumann', '18'],
                                       ['blake', 'howie', '30'],
                                       ['vanessa', 'parr', '29'],
                                       ['molly', 'roche', '15']],
                                 index=['dup_1', 'faux_dup_2', 'dup_3', 'faux_dup_4'],
                                 columns=['given_name', 'surname', 'age'])

predictions = pd.DataFrame(data=[1, 1, 0, 0],
                           index=pd.MultiIndex.from_arrays([['org_1', 'org_2', 'org_3', 'org_4'],
                                                            ['dup_1', 'faux_dup_2', 'dup_3', 'faux_dup_4']]),
                           columns=['label'])
true_links = pd.MultiIndex.from_arrays([['org_1', 'org_3'], ['dup_1', 'dup_3']])


def test_select_candidates_from_false_prediction_return_dataset_with_false_positive_when_false_positive_argument_is_True():
    # Given
    expected_result = pd.DataFrame(data=[['charles', 'green', '24'],
                                         ['blake', 'howie', '30']],
                                   index=['org_2', 'faux_dup_2'],
                                   columns=original_dataset.columns)

    # When
    result = select_candidates_from_false_prediction(predictions, true_links, original_dataset, duplicate_dataset, True)

    # Then
    assert_frame_equal(expected_result, result)


def test_select_candidates_from_false_prediction_return_dataset_with_false_positive_when_false_positive_argument_is_False():
    # Given
    expected_result = pd.DataFrame(data=[['vanessa', 'parr', '29'],
                                         ['vanessa', 'parr', '29']],
                                   index=['org_3', 'dup_3'],
                                   columns=original_dataset.columns)

    # When
    result = select_candidates_from_false_prediction(predictions, true_links, original_dataset, duplicate_dataset, False)

    # Then
    assert_frame_equal(expected_result, result)
