from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_BASE_PATH = BASE_DIR / "output"

def load_data_to_csv(df: pd.DataFrame, file_name: str, index_col: bool = False) :
    """
      Saves the cleaned DataFrame to a CSV file in the output directory.
    It reports the file's dimensions ( and the full path where the file was saved.
      """
    # print("==== DEBUG LOAD ====")
    # print("First 10 rows:\n", df.head(10))
    rows, cols = df.shape
    # print(df.shape)

    Full_Path = OUTPUT_BASE_PATH / file_name

    # Save DataFrame and handle errors
    try:
        df.to_csv(Full_Path, index=index_col)
        print("=" * 50 +
              f"\nThe **CLEAN, TRANSFORMED file** ('{Full_Path.name}') was successfully saved." +
              f"\nIt contains {rows} rows and {cols} columns." +
              f"\nAnd saved at: {Full_Path}")
        return str(Full_Path)
    except Exception as e:
        print(f"ERROR: Failed to save to CSV at {Full_Path}. Error: {e}")

