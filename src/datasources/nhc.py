from io import BytesIO

import pandas as pd

from src.utils import blob


def load_hist_fcast_monitors():
    return pd.read_parquet(
        BytesIO(
            blob.load_blob_data(
                f"{blob.PROJECT_PREFIX}//processed/monitors.parquet",
            )
        )
    )


def load_hti_distances():
    blob_name = f"{blob.PROJECT_PREFIX}/processed/noaa/nhc/historical_forecasts/hti_distances_2000_2023.parquet"
    print(blob_name)
    return pd.read_parquet(BytesIO(blob.load_blob_data(blob_name)))
