from configparser import ConfigParser
import os
import plotly.express as px
import warnings
import pandas as pd
warnings.filterwarnings("ignore")

def get_config(config_file):
    """
    Get config from config file
    """
    config = ConfigParser()
    config.read(config_file)
    data = {}
    for section in config.sections():
        if section != 'DEFAULT':
            for item in config.items(section):
                data[item[0]] = item[1]
    return data
            # yield section, config[section]
      

class department_graph:
    """
    Class to create a graph of departments
    """
    def __init__(self, df):
        self.df = df
        
    def create_graphs_bar(self):
        """
        create bar graphs for the department
        """
        for ind in self.df.index:
            dpt1 = self.df['department'][ind]
            dpt2 = self.df['department_2'][ind]
            if dpt1 == dpt2:
                self.df['department_2'][ind] = 'no'
                
        
        data_final = []
        departments = ['vocal artist', 'singer', 
                    'writer', 'artist', 'photographer', 'calligrapher',
                    'editor(text/video)', 'dancer', 'pr'
                    ]
        for department in departments:
            data_len = len(self.df[self.df['department'] == department]) + len(self.df[self.df['department_2'] == department])
            dataset = {}
            dataset['department'] = department
            dataset['member_count'] = data_len
            data_final.append(dataset)
        

        self.data = pd.DataFrame.from_dict(data_final)
        
        fig = px.bar(self.data, x='department', y='member_count', color='department',)
        fig.update_layout(title=f'{department}')
        
        return fig
        
    
    # def create_graph(self):
    #     """
    #     Create graph
    #     """
    #     for department in self.departments:
    #         self.graph[department] = []
    #         for item in self.departments[department]:
    #             self.graph[department].append(item)
    
    # def get_departments(self):
    #     """
    #     Get departments
    #     """
    #     return self.departments
    
    # def get_graph(self):
    #     """
    #     Get graph
    #     """
    #     return self.graph

