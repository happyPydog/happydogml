import numpy as np
import pandas as pd
import uuid


def generate_lag_data(
    sample_size=10,
    feature_size=3,
    lag_size=3,
    low=0,
    high=100,
    pk: str = "id",
):
    """
    Generate a dataframe with UUID index and lagged features.

    Parameters:
    - sample_size (int): Number of samples (rows).
    - feature_size (int): Number of features.
    - lag_size (int): Number of lagged versions per feature.
    - low (int): Lower bound for random values (for 'uniform' distribution).
    - high (int): Upper bound for random values (for 'uniform' distribution).
    - pk (str): Name of the primary key column.

    Example:
    >>> df = generate_lag_data(sample_size=3, feature_size=2, lag_size=2)
    >>> df
                                        feature1_l1m  feature1_l2m  feature2_l1m  feature2_l2m
    id
    f47a0d65-42d5-4c93-bb6b-3d38d8e24c6f      19          29          54          61
    62e76469-0e53-4347-91a4-5c39d1d1f089      72          15          33          48
    f418d4d7-7cb5-4e1f-9b6d-dcfb7d3281ef      38          48          13          88
    """
    uuids = [str(uuid.uuid4()) for _ in range(sample_size)]
    columns = {
        f"feature{feature}_l{lag}m": np.random.randint(
            low, high, size=sample_size
        )
        for feature in range(1, feature_size + 1)
        for lag in range(1, lag_size + 1)
    }

    df = pd.DataFrame(columns)
    df.index = uuids
    df.index.name = pk

    return df


if __name__ == "__main__":
    print(
        generate_lag_data(
            sample_size=5,
            feature_size=2,
            lag_size=12,
            low=0,
            high=100,
        )
    )
