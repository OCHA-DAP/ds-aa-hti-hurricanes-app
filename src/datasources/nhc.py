from io import BytesIO

import pandas as pd

from src.utils import blob


def load_hist_fcast_monitors():
    return pd.read_parquet(
        BytesIO(
            blob.load_blob_data(
                "ds-aa-hti-hurricanes/procesed/monitors.parquet",
                prod_dev="dev",
            )
        )
    )


def load_processed_historical_forecasts():
    return pd.read_csv(
        BytesIO(
            blob.load_blob_data(
                "processed/noaa/nhc/historical_forecasts/al_2000_2023.csv"
            )
        ),
        parse_dates=["issue_time", "valid_time"],
    )


def load_hti_distances():
    return pd.read_parquet(
        BytesIO(
            blob.load_blob_data(
                "processed/noaa/nhc/historical_forecasts/"
                "hti_distances_2000_2023.parquet"
            )
        )
    )
