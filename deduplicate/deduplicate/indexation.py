import pandas as pd
import recordlinkage
from recordlinkage.index import SortedNeighbourhood, Block


def block_indexing(blocking_key: list, original_dataset: pd.DataFrame,
                   duplicate_dataset: pd.DataFrame) -> pd.MultiIndex:
    """
    Simple function that use block indexation from deduplicate package.

    Make candidate record pairs, from original_dataset and duplicate_dataset, that agree on one or more variables
    of blocking_key parameter. Returns all record pairs founded.

    Parameters:
    -----------
        blocking_key (list) : A list of variables
        original_dataset (pandas.DataFrame) : A dataframe containing at least blocking_key variables in columns
        duplicate_dataset (pandas.DataFrame) : A dataframe containing at least blocking_key variables in columns
        true_links (pandas.MultiIndex) : MultiIndex of indexes' paire of candidtates, from between original_dataset
        and duplicate_dataset, which are same

    Return:
    --------
        pairs : pandas.MultiIndex with record pairs founded
    """
    indexer = recordlinkage.Index()
    for key in blocking_key:
        indexer.add(Block(left_on=key, right_on=key))
        pairs = indexer.index(original_dataset, duplicate_dataset)
        print("Nombre de paires sélectionnées: {}".format(len(pairs)))

    return pairs


def sorted_neighbourhood_indexing(sn_key: list, original_dataset: pd.DataFrame,
                                  duplicate_dataset: pd.DataFrame) -> pd.MultiIndex:
    """
    Simple function that use sorted neighbourhood indexation from deduplicate package.

    Make candidate record pairs, from original_dataset and duplicate_dataset, that agree on one or more variables
    of sn_key parameter. Returns all record pairs founded.

    Parameters:
    -----------
        sn_key (list) : A list of variables in which block method is made
        original_dataset (pandas.DataFrame) : A dataframe containing at least blocking_key variables in columns
        duplicate_dataset (pandas.DataFrame) : A dataframe containing at least blocking_key variables in columns
        true_links (pandas.MultiIndex) : MultiIndex of indexes' paire of candidtates, from between original_dataset
        and duplicate_dataset, which are same

    Return:
    --------
        pairs : pandas.MultiIndex with record pairs founded
    """
    indexer = recordlinkage.Index()
    for key in sn_key:
        indexer.add(SortedNeighbourhood(key))
        pairs = indexer.index(original_dataset, duplicate_dataset)
        print("Nombre de paires sélectionnées: {}".format(len(pairs)))

        return pairs


def selected_pairs_values(idx_pairs, original_dataset: pd.DataFrame, duplicate_dataset: pd.DataFrame):
    """
    Select row from orginal_dataset and duplicate_dataset matching with indexes in idx_pairs then return those
    rows concatenate in a dataframe.
    """
    candidates = pd.DataFrame(columns=original_dataset.columns)
    for tpl in idx_pairs:
        tmp_fst = original_dataset.iloc[original_dataset.index.isin([tpl[0]])]
        tmp_scd = duplicate_dataset.iloc[duplicate_dataset.index.isin([tpl[1]])]
        concat_tmp = pd.concat([tmp_fst, tmp_scd])
        candidates = pd.concat([candidates, concat_tmp])

    return candidates
