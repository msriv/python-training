# Convert column in dataframe to uppercase
import pandas as pd
 
def capitalize_column(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    df_copy = df.copy()
    if pd.api.types.is_string_dtype(df_copy[col_name]):
        df_copy[col_name] = df_copy[col_name].str.upper()
   
    return df_copy
    