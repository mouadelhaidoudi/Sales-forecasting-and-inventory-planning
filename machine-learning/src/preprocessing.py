import pandas as pd
from pathlib import Path


def preprocess(name , df : pd.DataFrame) :

    exportDir = Path(__file__).resolve().parent.parent / "data" / "cleaned"
    
    numCols = df.select_dtypes(include=["number"]).columns.tolist()
    
    if name == "calendar.csv" :
        
        df[numCols] = df[numCols].astype('Int64')

        for col in numCols :
            df[col] = df[col].fillna(df[col].median())

        event = ['event_name_1','event_type_2', 'event_name_2', 'event_type_1']
        for e in event :
            df[e] = df[e].fillna("N/A")
        
        df["date"] = pd.to_datetime(df["date"], format = "%Y-%m-%d", errors="coerce")
            
            
    
    if name == "sales_train_evaluation.csv" :
        for col in numCols :
            df[col] = df[col].fillna(0)
            
        
    # universale treatement
    
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
