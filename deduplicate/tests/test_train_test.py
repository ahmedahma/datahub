import pandas as pd

from deduplicate.train_test import train_test

data = pd.DataFrame({'col_1': ['val_1', '_val2', 'val_3'], 'col_2': ['val_4', 'val_5', 'val_6'], 'label': [0, 1, 1]})


def test_train_test_function_drop_label_column_from_X_train_dataset():
    # When
    actual_dic = train_test(data)

    # Then
    assert 'label' not in actual_dic['X_train'].columns


def test_train_test_function_drop_label_column_from_X_test_dataset():
    # When
    actual_dic = train_test(data)

    # Then
    assert 'label' not in actual_dic['X_test'].columns


def test_value_of_y_train_is_a_dataframe_with_only_one_column_named_label():
    # When
    actual_dic = train_test(data)

    # Then
    assert actual_dic['y_train'].columns == ['label']


def test_value_of_y_test_is_a_dataframe_with_only_one_column_named_label():
    # When
    actual_dic = train_test(data)

    # Then
    assert actual_dic['y_test'].columns == ['label']


def test_train_test_function_return_dic_with_correct_keys():
    expected_names = ['X_train', 'X_test', 'y_train', 'y_test']

    # When
    actual_names = list(train_test(data).keys())
    print(actual_names)
    diff = set(expected_names) ^ set(actual_names)

    # Then
    assert not diff
    assert len(set(actual_names)) == len(actual_names)
