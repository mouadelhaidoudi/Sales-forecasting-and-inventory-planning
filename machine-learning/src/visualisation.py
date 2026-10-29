import matplotlib.pyplot as plt
import pandas as pd

def vis(dataframes: dict[str, pd.DataFrame]) :
    df_cal = df_sales = df_sell =  df_sim = None
    for k,v in dataframes.items() :
            if k.startswith("calendar") :
                df_cal = dataframes[k]
            if k.startswith("sales_train_evaluation") :
                df_sales = dataframes[k]
            if k.startswith("sell_prices") :
                df_sell = dataframes[k]
            if k.startswith("simulated_inventory") :
                df_sim = dataframes[k]
                
                

    #sales_train_eval
                
    days = []
    for col in df_sales.columns :
        if col.startswith("d_") :
            days.append(col)
    
    df_sales["totalsales"] = df_sales[days].sum(axis=1)
    sales_per_item = (df_sales.groupby("dept_id", as_index=False)["totalsales"].sum())
    best_item = df_sales.loc[df_sales["totalsales"] == df_sales["totalsales"].max(), "item_id"].iloc[0]
    print(f"best item = {best_item}")
    
    x = sales_per_item["dept_id"]
    y = sales_per_item["totalsales"]
    plt.bar(x,y)
    plt.show()
