import pandas as pd
from pathlib import Path
from zipfile import ZipFile
import numpy as np

## data loading & exploration
machine_learning_dir = Path(__file__).resolve().parent.parent
data_dir = machine_learning_dir / "data"
archive_path = machine_learning_dir / "data.zip"

csv_files = [
    "calendar.csv",
    "sales_train_evaluation.csv",
    "sell_prices.csv",
    "simulated_inventory.csv",
]

if any(not (data_dir / file_name).exists() for file_name in csv_files):
    if not archive_path.exists():
        raise FileNotFoundError(f"Dataset archive not found: {archive_path}")

    data_dir.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive_path, "r") as archive:
        archive.extractall(data_dir)

df = pd.read_csv(data_dir / "calendar.csv", encoding="utf-8")
x = 10
print(df.head(x))
print(df.shape)
print(df.describe())
df.info()
print(df.isna().sum())
print(df.duplicated().sum())
print(df.describe())

## data preprocessing

numCols = ['wm_yr_wk','wday','month','year','snap_CA','snap_TX','snap_WI']
df[numCols] = df[numCols].astype('Int64')

for col in numCols :
    df[col] = df[col].map(
        lambda x : pd.NA if pd.isna(x) or x < 0 else x
    )


df = df.dropna()
df = df.drop_duplicates()

