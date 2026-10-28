import pandas as pd


def exploreData(name : str, df : pd.DataFrame, x=10) :
    
    print (f"showing info for ========= {name} ==========")
    print(df.head(x))
    print(df.shape)
    df.info()
    print(f"number of missings values{df.isna().sum()}")
    print(f"number of duplicates : {df.duplicated().sum()}")