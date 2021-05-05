import pandas as pd
from pandas.testing import assert_frame_equal

from deduplicate.indexation import block_indexing, selected_pairs_values

original_dataset = pd.DataFrame(index=['org_1', 'org_2'], data={'given_name': ['michaela', 'rachelle'],
                                                                'surname': ['neumann', 'luger'],
                                                                'age': [16, 21]})
duplicate_dataset = pd.DataFrame(index=['dup_1', 'dup_2'], data={'given_name': ['michaela', 'shella'],
                                                                 'surname': ['neumann', 'gruger'],
                                                                 'age': [60, 32]})


def test_block_indexing_function_return_correct_index_pairs_of_candidate_duplicated_if_there_is_duplication_between_original_dataset_and_duplicate_dataset():
    # Given
    key = ["given_name"]
    expected_pairs = pd.MultiIndex.from_arrays([['org_1'], ['dup_1']], names=['org', 'dup'])

    # When
    actual_pairs = block_indexing(key, original_dataset, duplicate_dataset)

    # Then
    assert actual_pairs == expected_pairs


def test_block_indexing_function_return_empty_multiindex_of_candidate_duplicted_if_there_is_no_duplication_between_original_dataset_and_duplicate_dataset():
    # Given
    key = ["age"]
    expected_pairs = []

    # When
    actual_pairs = block_indexing(key, original_dataset, duplicate_dataset)
    diff = set(expected_pairs) ^ set(actual_pairs)

    # Then
    assert not diff
    assert len(set(actual_pairs)) == len(actual_pairs)


def test_selected_pairs_values_return_dataframe_of_candidates_matching_with_indexes_given_in_idx_pairs_parameter():
    # Given
    idx_pairs = pd.MultiIndex.from_tuples([('org_1', 'dup_1')])
    expected_df = pd.DataFrame(index=['org_1', 'dup_1'], data={'given_name': ['michaela'] * 2,
                                                               'surname': ['neumann'] * 2,
                                                               'age': ['16', '60']})

    # When
    result_df = selected_pairs_values(idx_pairs, original_dataset, duplicate_dataset)
    result_df['age'] = result_df['age'].astype(str)

    # Then
    assert_frame_equal(result_df, expected_df)
