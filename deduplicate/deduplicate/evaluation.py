import pandas as pd

from recordlinkage import confusion_matrix
from sklearn.metrics import recall_score, precision_score, accuracy_score
from mlxtend.plotting import plot_confusion_matrix


def evaluation(Y_test: pd.DataFrame, predictions: pd.DataFrame):
    """
    Compute standard evaluation functions (recall, precision, accuracy) and plot confusion matrix.
    """
    recall = recall_score(Y_test, predictions)
    precision = precision_score(Y_test, predictions)
    accuracy = accuracy_score(Y_test, predictions)

    print("Rappel: {}".format(recall))
    print("Precision: {}".format(precision))
    print("Accuracy: {}".format(accuracy))
    print("0: match \n1: non match")
    plot_confusion_matrix(confusion_matrix(Y_test, predictions))

    return recall, precision, accuracy


def select_candidates_from_false_prediction(predictions: pd.DataFrame, true_links: pd.MultiIndex,
                                            original_dataset: pd.DataFrame, duplicate_dataset: pd.DataFrame,
                                            false_positive=True):
    """
    Select false positive (or true positive) candidate predicted and return a dataframe with these candidate.

    Parameters:
    -----------
        predictions (pd.MutliIndex) :
        true_links (pandas.MultiIndex) :  MultiIndex of indexes' paire of candidtates, from between original_dataset
        and duplicate_dataset, which are same
        original_dataset (pandas.DataFrame) :  A dataframe containing at least feature_to_comp
        duplicate_dataset (pandas.DataFrame) :  A dataframe containing at least feature_to_comp
        test (pandas.DataFrame) :  DataFrame used to train the classifer
        false_positive (bool) : prediction to select

    Return:
    -----------
        (pandas.DataFrame) : A dataframe with false positive (or false negatif)
    """

    if false_positive:
        match_prediction = predictions[predictions['label'] == 1]
        false = list(set(match_prediction.index.values) - set(true_links.values))
        false = list(zip(*false))
    else:
        non_match_prediction = predictions[predictions['label'] == 0]
        false = list(set(non_match_prediction.index.values).intersection(set(true_links.values)))
        false = list(zip(*false))  # format change

    candidate_fst_idx = original_dataset.iloc[original_dataset.index.isin(false[0])]
    candidate_scd_idx = duplicate_dataset.iloc[duplicate_dataset.index.isin(false[1])]

    return pd.concat([candidate_fst_idx, candidate_scd_idx])