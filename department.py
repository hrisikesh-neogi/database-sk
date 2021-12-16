"""
giving department name it'll return the template accordingly
"""
import pandas as pd
from sending_Class import mongo_operation
from utils import get_config
from plotly_Dashboard.index import plotly_Dashboard
from flask import render_template

client = get_config('config.ini')

class department:
    """params:
    joiningAs : members table of which the member joining as
    joiningAs lists: {'vocal artist', 'singer', 
                    'writer', 'artist', 'photographer', 'calligrapher',
                    'editor(text/video)', 'dancer', 'pr'
                    }


    """

    def __init__(self,joiningAs):
        self.joiningAs = joiningAs
        self.db = mongo_operation(client['client_url'], client['database'])
        self.data = self.db.find(collection_name = 'original_member_data', query = {})

    def get_values_col(self):
        """Returns
        columns and values of the dataframe
        to show them in the table
        
        
        """
        
        

        if self.data.empty:

            return self.data.columns, self.data.values
        else:
            for ind in self.data.index:
                dpt1_ = self.data['department'][ind]
                dpt2_ = self.data['department_2'][ind]
                if dpt1_ == dpt2_:
                    self.data['department_2'][ind] = 'no'

            self.origin = ['vocal artist', 'singer', 
                            'writer', 'artist', 'photographer', 'calligrapher',
                            'editor(text/video)', 'dancer', 'pr']
                    




            columns = self.data.columns
            dpt1 = self.data[self.data['department'] == self.joiningAs]
            dpt2 = self.data[self.data['department_2'] == self.joiningAs]
            dpt = pd.concat([dpt1, dpt2])
            dpt = dpt.reset_index(drop=True)
            values = [[dpt.loc[i, col] for col in dpt.columns ] for i in range(len(dpt)) ]
            return columns, values

    # def department_graph(self):
    #     """
    #     Create graph
    #     """
    #     self.graph = {}
    #     for department in self.origin:
    #         self.graph[department] = []
    #         for item in self.data[self.data['department'] == department]:
    #             self.graph[department].append(item)
    #             self.graph[department].append(item)

    # def department_graph(self):
    def pr_data(self):
    
        pr = self.db.find(collection_name = 'sk_pr', query = {})

        final = {}
        for i in range(len(pr)):
            names = self.data[self.data['Pr'] == pr['Name'][i]]['name']
            dataset = [data for data in names]
            final[pr["Name"][i]] = {dataset.index(name) : name for name in dataset }
        
        final_Data = pd.DataFrame.from_dict(final)
        final_Data = final_Data.fillna(0)
        values = [[final_Data.loc[i, col] for col in final_Data.columns ] for i in range(len(final_Data)) ]
        columns = final_Data.columns

        return columns, values

        


def department_graph( app):
    """
    app = flaskapp
    returns plot
    """
    try:
        data = pd.read_csv('dataset/data.csv')
        plotly_Dashboard(app, data = data )

    except FileNotFoundError:
        print('No file found')
        return render_template ('404.html')
    