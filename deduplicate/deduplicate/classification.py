import pandas as pd
from codecarbon import EmissionsTracker


def add_label(scores: pd.DataFrame, true_links: pd.MultiIndex) -> pd.DataFrame:
    """
    Generate two new columns :
        - tupled_index : concatenation of scores dataframe index
        - label : 1 if the candidate pair is a real match, 0 otherwise
    And then drop column tupled_index

    Parameters:
    -----------
        scores (pandas.DataFrame) : A DataFrame with scores vectors
        true_links (pandas.MultiIndex) :  MultiIndex of indexes' paire of candidtates, from between original_dataset
        and duplicate_dataset, which are same
        and duplicate_dataset, which are same

    Return:
    -----------
        score_with_label (pandas.DataFrame) : A dataframe containing 1 new column 'label'
    """

    score_with_label = scores.copy()
    score_with_label['tupled_index'] = score_with_label.index.tolist()
    score_with_label['label'] = score_with_label['tupled_index'].apply(lambda x: 1 if x in true_links else 0)
    score_with_label = score_with_label.drop('tupled_index', axis=1, inplace=False)

    return score_with_label


def fit_and_track(project_name: str, clf, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.DataFrame):
    """
    Train and fit the classifier clf with X_train, X_test and y_train and calculate carbon emissions
    using EmissionsTracker from codecarbon

    Parameters:
    -----------
        project_name (str) : Name of the project for EmissionTracker function
        X_train (pandas.DataFrame) : A DataFrame for training
        X_test (pandas.DataFrame) : A DataFrame for test
        y_train (pandas.DataFrame) : A DataFrame for training

    Return:
    -----------
        predictions (numpy.array) : Array of predicted values

    """
    tracker = EmissionsTracker(project_name=project_name)
    tracker.start()

    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)

    tracker.stop()

    return predictions
