from pathlib import Path
import pandas as pd

def save_dataframe(df: pd.DataFrame, output_folder: Path, filename: str):
    """
    Save a DataFrame as CSV and print useful information.
    """
    output_file = output_folder / filename

    df.to_csv(output_file, index=False)

    print(f"✅ Saved: {filename}")
    print(f"   Rows    : {len(df)}")
    print(f"   Columns : {len(df.columns)}")
    print(f"   Location: {output_file}\n")