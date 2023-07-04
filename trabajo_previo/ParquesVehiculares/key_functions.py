from typing import List, Iterable, Set
from itertools import chain, combinations
import pandas as pd
from tqdm import tqdm


def flatten_set(set_: set) -> set:
    """Flatten a set of sets."""
    return set(chain.from_iterable(set_))


def extract_canditate_keys(df: pd.DataFrame) -> list[str]:
    """Extract the candidate keys from a DataFrame."""
    n = len(df.columns)
    candidate_keys = []
    for i in tqdm(range(1, n + 1), desc='Extracting candidate keys', total=n):
        # if i > 1:
        #     break
        keys_to_check = set(df.columns) - flatten_set(candidate_keys)
        for key in combinations(keys_to_check, i):
            subset = set(key)
            if subset in candidate_keys:
                continue
            
            # Check if the key is a candidate key
            if not df[list(subset)].duplicated().any():
                candidate_keys.append(subset)
    return candidate_keys

            
def get_power_set(iterable: Iterable) -> Iterable:
    """Get the power set of an iterable."""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))

def extract_super_keys(df: pd.DataFrame) -> Iterable:
    """Extract the super keys from a DataFrame.
    A super key is a set of columns that uniquely identify each row.
    """
    n = len(df)
    columns_combinations = get_power_set(df.columns)
    for columns in columns_combinations:
        if len(df.groupby(list(columns))) == n:
            yield list(columns)
            
            
def preserve_minimal_subsets(subsets: Iterable[Set], pbar: tqdm = None) -> List[Set]:
    subsets = sorted(subsets, key=len)
    
    minimal_subsets = set()
    
    for subset in subsets:
        if any (subset < minimal_subset for minimal_subset in minimal_subsets):
            if pbar:
                pbar.update(1)
            continue
        minimal_subsets.add(subset)
        if pbar:
            pbar.update(1)
    
    return minimal_subsets


def get_candidate_keys(df: pd.DataFrame, pbar: bool = False) -> List[Set]:
    """Get the candidate keys of a DataFrame.
    A candidate key is a minimal super key.
    """
    super_keys = extract_super_keys(df)
    pbar = tqdm(total=len(df.columns)**2) if pbar else None
    candidate_keys = preserve_minimal_subsets(super_keys, pbar)
    return candidate_keys

