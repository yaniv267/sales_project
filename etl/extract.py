import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path


#  Dataset Configuration
KAGGLE_DATASET_NAME = 'yusufdelikkaya/online-sales-dataset'
CSV_FILE_NAME = "online_sales_dataset.csv"

#  Define Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DOWNLOAD_PATH = BASE_DIR / "data"

def extract_data():
    """
        Downloads the specified dataset file from Kaggle and loads the
        resulting CSV file The function validates the download,
        and returns the DataFrame.
        """
    #  Initialize Kaggle API
    print("=== Initializing Kaggle API ====")

    api = KaggleApi()
    api.authenticate()
    #  Download Dataset from Kaggle
    print("=== Starting Dataset Download from Kaggle ===")
    try:
        api.dataset_download_files(
            KAGGLE_DATASET_NAME,
            path=DOWNLOAD_PATH,
            unzip=True
        )
        print(f"Download completed and located at path: {DOWNLOAD_PATH}")
    except Exception as e:
        print("Error downloading dataset from Kaggle")
        print(f"Reason: {e}")
        return None

    #  Verify CSV Exists After Download
    csv_path = DOWNLOAD_PATH / CSV_FILE_NAME
    if not csv_path.exists():
        print(f"CSV file '{CSV_FILE_NAME}' not found after download.")
        return None
    # Load CSV

    print(f"===== Starting Extraction of '{CSV_FILE_NAME}' =====")
    try:
        df = pd.read_csv(csv_path)
        rows, cols = df.shape
        print(
            f"The file '{CSV_FILE_NAME}' was extracted successfully.\n"
            f"It contains {rows} rows and {cols} columns.\n"
            f"File location: {csv_path}"
        )
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

