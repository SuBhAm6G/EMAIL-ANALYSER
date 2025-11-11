import pandas as pd
def load_csv(filepath):
    df=pd.read_csv(filepath, parse_dates=['date'], dayfirst=True)
    return df
