import numpy as np
import pandas as pd
from src.tools.paths import dimensions_path, datasets_path


def read_data_to_df(type: str, name: str):
    if type == 'dataset':
        path = datasets_path(f"{name}.csv")
    else:
        raise RuntimeError(f"Invalid type {type}.")
    data = pd.read_csv(path)
    return data


def read_data_to_list(type: str, name: str, dtype: type):
    if type == 'dimension':
        path = dimensions_path(f"{name}.csv")
    else:
        raise RuntimeError(f"Invalid type {type}.")
    data = np.loadtxt(path, dtype=dtype, delimiter=';').tolist()
    # catch size one lists, which are transformed to scalar by np.ndarray.tolist()
    data = data if isinstance(data, list) else [data]
    return data