import pandas as pd
from pandas.testing import assert_frame_equal

from deduplicate.classification import add_label

scores = pd.DataFrame(data=[[1, 1, 1], [0, 0, 0]],
                      index=pd.MultiIndex.from_arrays([['org_1', 'org_1'], ['dup_1', 'dup_2']]),
                      columns=['given_name_score', 'surname_score', 'age_score'])
true_links = pd.MultiIndex.from_tuples([('org_1', 'dup_1')])


def test_add_label_function_correctly_add_the_new_column_named_label():
    # Given
    expected_columns = scores.columns.tolist() + ['label']

    # When
    actual_columns = add_label(scores, true_links).columns
    diff = set(expected_columns) ^ set(actual_columns)

    # Then
    assert not diff
    assert len(set(actual_columns)) == len(actual_columns)


def test_add_label_function_return_dataset_with_correct_values():
    # Given
    expected_df = scores
    expected_df['label'] = [1, 0]

    # When
    result = add_label(scores, true_links)

    # Then
    assert_frame_equal(result, expected_df)
