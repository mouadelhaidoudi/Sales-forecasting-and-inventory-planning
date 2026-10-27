import pandas as pd


def exploreData(df, x=10) :
    
    print(df.head(x))
    print(df.shape)
    print(df.describe())
    df.info()
    print(df.isna().sum())
    print(df.duplicated().sum())
    print(df.describe())