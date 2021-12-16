from data_pre import *
import pandas as pd

def members_data_pre(df):
    """
    for members' dataset cleaning
    
    """

    object = df_preprocessing(df)
    final_Df = object.dropping_col()
    final_Df.to_csv('./data_out/members.csv')
    final_Df.to_csv('./static/data.csv', index=False)
    data_values = object.df_to_list()
    return final_Df, data_values



def writers_data_pre(path):
    """
    for writers' dataset cleaning
    
    """
    df = pd.read_csv(path)
    object = writer_dst(df)
    #changing column names
    object.col_name_change()
    
    #changing data types
    #final preprocessed data
    final_Df = object.preprocessing()    
    return final_Df

def writers_final(df): 
    """
    saves the data into folder and
    returns the data in list format and the dataframe column names
    
    """
    # delete first column
    df = df.drop(df.columns[0], axis=1)

    df.to_csv('./writers_Raw/writers_data.csv', index=False)
    df.to_csv('./static/data.csv', index=False)

    final_Data = [[df.loc[i, col] for col in df.columns ] for i in range(len(df)) ]
    return final_Data, df.columns
