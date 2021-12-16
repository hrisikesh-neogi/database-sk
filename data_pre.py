import pandas as pd

columns = ['Email Address', 'Name', 'Address', 'phoneNo_wp', 'callingNo',
           'Date of joining Shohure Kotha ', 'Date of Birth', 'Occupation ',
           'Hobbies / Interests ', 'You are joining as a ',
           'except shohure kotha, name the pages you are working at  - ',
           'agree with rules']


class df_preprocessing():
    def __init__(self, df):
        self.df =  df
        
    def df_columns(self):
        return self.df.columns     #returns the column names of the dataframe   
    def dropping_col(self):


        columns_to_Drop = [self.df.columns[0], self.df.columns[1], self.df.columns[9], self.df.columns[10]]
        for col in self.df.columns[16:]:
            columns_to_Drop.append(col)
        self.out_data = self.df.drop( columns = columns_to_Drop)

        columns = ['Email Address', 'Name', 'Address', 'phoneNo_wp', 'callingNo',
           'Date of joining Shohure Kotha ', 'Date of Birth', 'Occupation ',
           'Hobbies / Interests ', 'You are joining as a ',
           'except shohure kotha, name the pages you are working at  - ',
           'agree with rules']

        self.out_data.columns = columns
        return self.out_data
    
    def df_to_list(self):
        final_Data = [[self.out_data.loc[i, col] for col in self.out_data.columns ] for i in range(len(self.out_data)) ]
        return final_Data


class writer_dst():

    """ preprocessing the data of sk writers
    
    """
    def __init__(self, df):
        self.df = df

    def col_name_change(self):
        columns_to_change = self.df.columns[2:]
        column_name = []
        for i in range(len(columns_to_change)):
            column_name.append(f'WEEK_{i+1}')

        for i in range(len(self.df.columns[0:2])):
            column_name.insert(i, self.df.columns[i])

        self.df.columns = column_name
        return self.df

    

    
    def preprocessing(self):
        
         #dropping the first row
        self.df = self.df.iloc[1:,:]
        self.df = self.df.reset_index(drop = True)
        
        # dropping the whole null rows
        index_to_drop = []
        for i in range(len(self.df)):
            if self.df.iloc[i:i+1].isna().sum().sum() == len(self.df.columns):
                index_to_drop.append(i)
        print(index_to_drop)
        self.df = self.df.drop(index =  index_to_drop)
        self.df = self.df.reset_index(drop = True)

        
        self.df = self.df.fillna(0)
        for column in self.df.columns.values:
            if self.df[column].dtypes == 'float':
                self.df[column] = self.df[column].astype(int)

       
            
        
        #splliting the name column
        self.df['NAMES'] = self.df['NAMES'].str.split('.')
        self.df['NAMES'] = self.df['NAMES'].apply(lambda x : x[1])
        self.df['NAMES'] = self.df['NAMES'].apply(lambda x : str(x))
        
        return self.df

