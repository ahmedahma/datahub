import recordlinkage
import pandas as pd


def comparison_scores(attr: list, candidate_pairs: pd.MultiIndex, original_dataset: pd.DataFrame,
                      duplicate_dataset: pd.DataFrame, method:list=None) -> pd.DataFrame:
    """
    Compare the attributes of candidate record pairs candidate_pairs and return scores comparison
    returned by .compute() method from recordlinkage.


    Parameters:
    -----------
        attr (list) : List of attributes to compare
        candidate_pairs (pandas.MultiIndex) :  MultiIndex with index of candidate pairs to compare
        original_dataset (pandas.DataFrame) : A dataframe containing at least feature_to_comp variables
        duplicate_dataset (pandas.DataFrame) :  A dataframe containing at least feature_to_comp variables
        method (list) : list of method (jarowinkler, leveinshtein, etc) to use for comparison

    Return:
    --------
        scores (pandas.DataFrame) : A DataFrame with the comparison scores vectors
    """
    compare = recordlinkage.Compare()
    # initialise similarity measurement algorithms
    if method is None:
        method = ['jarowinkler']*len(attr)

    for i in range(len(attr)):
        compare.string(attr[i], attr[i], label=attr[i] + '_score', method=method[i])

    # the method .compute() returns the DataFrame with the feature vectors.
    scores = compare.compute(candidate_pairs, original_dataset, duplicate_dataset)

    return scores