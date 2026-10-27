import pandas as pd
from pathlib import Path


def preprocess(name , df : pd.DataFrame) :

    exportDir = Path(__file__).resolve().parent.parent / "data" / "cleaned"
    
    if name == "calendar.csv" :
        numCols = ['wm_yr_wk','wday','month','year','snap_CA','snap_TX','snap_WI']
        df[numCols] = df[numCols].astype('Int64')

        for col in numCols :
            df[col] = df[col].map(
                lambda x : pd.NA if pd.isna(x) or x < 0 else x
            )

        event = ['event_name_1','event_type_2', 'event_name_2', 'event_type_1']
        for e in event :
            df[e] = df[e].fillna("N/A")
        
    df = df.dropna()
    df = df.drop_duplicates()
    
    try :
        name = name.replace(".csv","_CLEANED.csv")
        exp = exportDir / name
        df.to_csv(exp, index = False)
    except Exception as e: 
        print(f"something wrong happened while exporting : {exp}")
        print(f"Exception : {e}")
        raise
    else :
        print("successfuly exported : "+str(exp))
        return name, df
