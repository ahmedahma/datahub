def browse_datasets():
    pass


def test_browse_datasets_returns_correct_list_of_datasets():
    # Given
    expected_json = {}

    # When
    actual_json = browse_datasets()
    
    # Then
    assert expected_json == actual_json

