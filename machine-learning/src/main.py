import pandas as pd
from pathlib import Path
from zipfile import ZipFile
import numpy as np
import exploration
import preprocessing

# temp commands
LoadRawData = True

## data loading
machine_learning_dir = Path(__file__).resolve().parent.parent
data_dir = machine_learning_dir / "data"
cleaned_data_dir = data_dir / "cleaned"
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

dataframes = {}
for name in csv_files :
    try :
        name = name if LoadRawData else name.replace(".csv", "_CLEANED.csv")
        df = pd.read_csv((data_dir if LoadRawData else cleaned_data_dir) / name, encoding="utf-8")
    except Exception as e :
        print(f"failed to import {data_dir}\\{name}, raised exception {e}")
        continue
    dataframes[name] = df

        
#data exloration
for name,df in dataframes.items() :
    exploration.exploreData(name,df)

# data preprocessing
if  LoadRawData :
    dataframes_cleaned = {}
    for name,df in dataframes.items() :
        try :
            name , cdf = preprocessing.preprocess(name,df)
        except Exception as e :
            print(f"preprocessing failed for {name}, Exception raised : {e}")
            continue
        dataframes_cleaned[name] = cdf


## data visualisation 

