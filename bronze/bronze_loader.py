from pathlib import Path

import pandas as pd

from config import BRONZE_DATA_DIR, RAW_DATA_DIR


def load_raw_csv(file_name: str) -> pd.DataFrame:
    """
    Load a raw CSV file and add Bronze-layer ingestion metadata.

    Parameters
    ----------
    file_name:
        Name of the CSV file stored in data/raw.

    Returns
    -------
    pd.DataFrame
        Raw dataset with ingestion metadata columns.
    """
    source_path = RAW_DATA_DIR / file_name

    if not source_path.exists():
        raise FileNotFoundError(f"Raw source file not found: {source_path}")

    dataframe = pd.read_csv(source_path)

    dataframe["_source_file"] = file_name
    dataframe["_ingestion_timestamp"] = pd.Timestamp.now(tz="UTC")
    dataframe["_record_source"] = "synthetic_retail_generator"

    return dataframe


def write_bronze_parquet(
    dataframe: pd.DataFrame,
    table_name: str,
) -> Path:
    """
    Write a DataFrame to the local Bronze layer in Parquet format.

    Parameters
    ----------
    dataframe:
        Dataset to write.

    table_name:
        Bronze table name without the file extension.

    Returns
    -------
    Path
        Path of the written Parquet file.
    """
    if dataframe.empty:
        raise ValueError(f"Cannot write empty Bronze dataset: {table_name}")

    output_path = BRONZE_DATA_DIR / f"{table_name}.parquet"

    dataframe.to_parquet(
        output_path,
        index=False,
    )

    output_path = BRONZE_DATA_DIR / f"{table_name}.parquet"

    dataframe.to_parquet(
        output_path,
        index=False,
    )

    return output_path

# import pandas as pd

# from config import BRONZE_DATA_DIR, RAW_DATA_DIR


# def load_raw_csv(file_name: str) -> pd.DataFrame:
#     """
#     Load a raw CSV file and add Bronze-layer ingestion metadata.

#     Parameters
#     ----------
#     file_name:
#         Name of the CSV file stored in data/raw.

#     Returns
#     -------
#     pd.DataFrame
#         Raw dataset with ingestion metadata columns.
#     """
#     source_path = RAW_DATA_DIR / file_name

#     if not source_path.exists():
#         raise FileNotFoundError(f"Raw source file not found: {source_path}")

#     dataframe = pd.read_csv(source_path)

#     dataframe["_source_file"] = file_name
#     dataframe["_ingestion_timestamp"] = pd.Timestamp.now(tz="UTC")
#     dataframe["_record_source"] = "synthetic_retail_generator"

#     return dataframe


# def write_bronze_parquet(
#     dataframe: pd.DataFrame,
#     table_name: str,
# ) -> Path:
#     """
#     Write a DataFrame to the local Bronze layer in Parquet format.

#     Parameters
#     ----------
#     dataframe:
#         Dataset to write.

#     table_name:
#         Bronze table name without the file extension.

#     Returns
#     -------
#     Path
#         Path of the written Parquet file.
#     """
#     if dataframe.empty:
#         raise ValueError(f"Cannot write empty Bronze dataset: {table_name}")

#     output_path = BRONZE_DATA_DIR / f"{table_name}.parquet"

#     dataframe.to_parquet(
#         output_path,
#         index=False,
#     )

#     return output_path