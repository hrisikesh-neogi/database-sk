import dash
from dash import html
from dash import dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sending_Class import mongo_operation
# from datetime import datetime
from member_detail import *
from configparser import ConfigParser 
from utils import get_config, department_graph
from datetime import datetime



# from sending_Class import mongo_operation

# from member_detail import *
# from utils import get_config

# config = get_config('config.ini')

# db = mongo_operation(config['client_url'], config['database'])
# data = db.find('original_member_data', {} )
# art = len(data[data['department']=='art']) + len(data[data['department_2'] == 'artist'] )
# writing = len(data[data['department']=='writing']) + len(data[data['department_2'] == 'writer'] )
# photography = len(data[data['department']=='photography']) + len(data[data['department_2'] == 'photographer'] )
# singer = len(data[data['department']=='music']) + len(data[data['department_2'] == 'singer'] )
# fig = px.bar(data, x='department', color='department', barmode='group')




def plotly_Dashboard(flask_app, data):
    graph = department_graph(data)
    fig= graph.create_graphs_bar()
    app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                server=flask_app,
            # name = "dashboard",
            url_base_pathname='/dashboard/charts/',)

    app.layout = html.Div([
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('sklogo.jpg'),
                        id='corona-image',
                        style={
                            "height": "60px",
                            "width": "auto",
                            "margin-bottom": "25px",
                        },
                        )
            ],
                className="one-third column",
            ),
            html.Div([
                html.Div([
                    html.H3("Shohure Kotha Dashboard", style={"margin-bottom": "0px", 'color': 'white'}),
                    html.H5("Track Member Records", style={"margin-top": "0px", 'color': 'white'}),
                ])
            ], className="one-half column", id="title"),

            html.Div([
                html.H6('Last Updated: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        style={'color': 'orange'}),

            ], className="one-third column", id='title1'),

        ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

        html.Div([
            html.Div([
                html.H6(children='Total members',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
                        ),

                html.P(f"{len(data)}",
                    style={
                        'textAlign': 'center',
                        'color': 'orange',
                        'fontSize': 40}
                    ),

                # html.P('new:  ' + f"{covid_data_1['total'].iloc[-1] - covid_data_1['total'].iloc[-2]:,.0f} "
                #     + ' (' + str(round(((covid_data_1['total'].iloc[-1] - covid_data_1['total'].iloc[-2]) /
                #                         covid_data_1['total'].iloc[-1]) * 100, 2)) + '%)',
                #     style={
                #         'textAlign': 'center',
                #         'color': 'orange',
                #         'fontSize': 15,
                #         'margin-top': '-18px'}
                #     )
                ], className="card_container three columns",
            ),

            html.Div([
                html.H6(children='Total Writers',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
                        ),

                html.P(f"{len(data[data['department']=='writer']) + len(data[data['department_2'] == 'writer'] )}",
                    style={
                        'textAlign': 'center',
                        'color': '#dd1e35',
                        'fontSize': 40}
                    ),

                # html.P('new:  ' + f"{covid_data_1['death'].iloc[-1] - covid_data_1['death'].iloc[-2]:,.0f} "
                #     + ' (' + str(round(((covid_data_1['death'].iloc[-1] - covid_data_1['death'].iloc[-2]) /
                #                         covid_data_1['death'].iloc[-1]) * 100, 2)) + '%)',
                #     style={
                #         'textAlign': 'center',
                #         'color': '#dd1e35',
                #         'fontSize': 15,
                #         'margin-top': '-18px'}
                #     )
                ], className="card_container three columns",
            ),

            html.Div([
                html.H6(children='Vocal Artists',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
                        ),

                html.P(f"{len(data[data['department']=='vocal artist']) + len(data[data['department_2'] == 'vocal artist'] )}",
                    style={
                        'textAlign': 'center',
                        'color': 'green',
                        'fontSize': 40}
                    ),

                html.P('singer:  ' + f"{len(data[data['department']=='singer']) + len(data[data['department_2'] == 'singer'])} "
                    ,
                    style={
                        'textAlign': 'center',
                        'color': 'green',
                        'fontSize': 15,
                        'margin-top': '-18px'}
                    )
                    ], className="card_container thr  ee columns",
            ),

            html.Div([
                html.H6(children='Art And Photography',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
                        ),

                html.P("Artist:" +"   " f"{len(data[data['department']=='artist']) + len(data[data['department_2'] == 'artist'] )}",
                    style={
                        'textAlign': 'center',
                        'color': '#e55467',
                        'fontSize': 40}
                    ),

                html.P('Photographers:  ' + f"{len(data[data['department'] == 'photography']) + len(data[data['department_2'] == 'photographer'])}"
                    ,
                    style={
                        'textAlign': 'center',
                        'color': '#e55467',
                        'fontSize': 15,
                        'margin-top': '-18px'}
                    )], className="card_container three columns")

        ], className="row flex-display"),

        html.Div([
            html.Div([

                        # html.P('Select Country:', className='fix_label',  style={'color': 'white'}),

                        # dcc.Dropdown(id='departments',
                        #             multi=False,
                        #             clearable=True,
                        #             value='department',
                        #             placeholder='Select Department',
                        #             options=[{'label': c, 'value': c}
                        #                     for c in (data['department'].unique())], className='dcc_compon')
                        #                     ,

                        html.P('New Members : ' + '  ' + ' ' + str(data['name'].iloc[-1]) + '  ', className='fix_label',  style={'color': 'white', 'text-align': 'center'}), 
                        dcc.Graph(
                        id='example-graph',
                        figure=fig
                    )
                        
                        ] )
        ])
    ])
                        # dcc.Graph(id='total', config={'displayModeBar': False}, className='dcc_compon',
                        # style={'margin-top': '20px'},
                        # ),

                        # dcc.Graph(id='death', config={'displayModeBar': False}, className='dcc_compon',
                        # style={'margin-top': '20px'},
                        # ),

                        # dcc.Graph(id='recovered', config={'displayModeBar': False}, className='dcc_compon',
                        # style={'margin-top': '20px'},
                        # ),

                        # dcc.Graph(id='active', config={'displayModeBar': False}, className='dcc_compon',
                        # style={'margin-top': '20px'},
                        # )
                        # ,

    #         ], className="create_container three columns", id="cross-filter-options"),
    #             html.Div([
    #                     dcc.Graph(id='pie_chart',
    #                             config={'displayModeBar': 'hover'}),
    #                             ], className="create_container four columns"),

    #                     html.Div([
    #                         dcc.Graph(id="line_chart")

    #                     ], className="create_container five columns"),

    #         ], className="row flex-display"),

    # html.Div([
    #         html.Div([
    #             dcc.Graph(id="map")], className="create_container1 twelve columns"),

    #             ], className="row flex-display"),

    #     ], id="mainContainer",
    #     style={"display": "flex", "flex-direction": "column"})

    # @app.callback(
    #     Output('total', 'figure'),
    #     [Input('departments', 'value')])
    # def update_total(departments, value):

    #     total_members = len(data[data[departments] == value])
    #     return {
    #             'data': [go.Indicator(
    #                     mode='number+delta',
    #                     value=total_members,
                        
    #                     number={'valueformat': ',',
    #                             'font': {'size': 20},

    #                             },
    #                     domain={'y': [0, 1], 'x': [0, 1]})],
    #             'layout': go.Layout(
    #                 title={'text': 'New total',
    #                     'y': 1,
    #                     'x': 0.5,
    #                     'xanchor': 'center',
    #                     'yanchor': 'top'},
    #                 font=dict(color='orange'),
    #                 paper_bgcolor='#1f2c56',
    #                 plot_bgcolor='#1f2c56',
    #                 height=50
    #                 ),

    #             }

    # @app.callback(
    #     Output('death', 'figure'),
    #     [Input('w_countries', 'value')])
    # def update_total(w_countries):
    #     covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['total', 'death', 'recovered', 'active']].sum().reset_index()

    #     value_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-2]
    #     delta_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-3]
    #     return {
    #             'data': [go.Indicator(
    #                     mode='number+delta',
    #                     value=value_death,
    #                     delta={'reference': delta_death,
    #                             'position': 'right',
    #                             'valueformat': ',g',
    #                             'relative': False,

    #                             'font': {'size': 15}},
    #                     number={'valueformat': ',',
    #                             'font': {'size': 20},

    #                             },
    #                     domain={'y': [0, 1], 'x': [0, 1]})],
    #             'layout': go.Layout(
    #                 title={'text': 'New Death',
    #                     'y': 1,
    #                     'x': 0.5,
    #                     'xanchor': 'center',
    #                     'yanchor': 'top'},
    #                 font=dict(color='#dd1e35'),
    #                 paper_bgcolor='#1f2c56',
    #                 plot_bgcolor='#1f2c56',
    #                 height=50
    #                 ),

    #             }

    # @app.callback(
    #     Output('recovered', 'figure'),
    #     [Input('w_countries', 'value')])
    # def update_total(w_countries):
    #     covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['total', 'death', 'recovered', 'active']].sum().reset_index()

    #     value_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2]
    #     delta_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-3]
    #     return {
    #             'data': [go.Indicator(
    #                     mode='number+delta',
    #                     value=value_recovered,
    #                     delta={'reference': delta_recovered,
    #                             'position': 'right',
    #                             'valueformat': ',g',
    #                             'relative': False,

    #                             'font': {'size': 15}},
    #                     number={'valueformat': ',',
    #                             'font': {'size': 20},

    #                             },
    #                     domain={'y': [0, 1], 'x': [0, 1]})],
    #             'layout': go.Layout(
    #                 title={'text': 'New Recovered',
    #                     'y': 1,
    #                     'x': 0.5,
    #                     'xanchor': 'center',
    #                     'yanchor': 'top'},
    #                 font=dict(color='green'),
    #                 paper_bgcolor='#1f2c56',
    #                 plot_bgcolor='#1f2c56',
    #                 height=50
    #                 ),

    #             }

    # @app.callback(
    #     Output('active', 'figure'),
    #     [Input('w_countries', 'value')])
    # def update_total(w_countries):
    #     covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['total', 'death', 'recovered', 'active']].sum().reset_index()

    #     value_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2]
    #     delta_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-3]
    #     return {
    #             'data': [go.Indicator(
    #                     mode='number+delta',
    #                     value=value_active,
    #                     delta={'reference': delta_active,
    #                             'position': 'right',
    #                             'valueformat': ',g',
    #                             'relative': False,

    #                             'font': {'size': 15}},
    #                     number={'valueformat': ',',
    #                             'font': {'size': 20},

    #                             },
    #                     domain={'y': [0, 1], 'x': [0, 1]})],
    #             'layout': go.Layout(
    #                 title={'text': 'New Active',
    #                     'y': 1,
    #                     'x': 0.5,
    #                     'xanchor': 'center',
    #                     'yanchor': 'top'},
    #                 font=dict(color='#e55467'),
    #                 paper_bgcolor='#1f2c56',
    #                 plot_bgcolor='#1f2c56',
    #                 height=50
    #                 ),

    #             }

    # # Create pie chart (total casualties)
    # @app.callback(Output('pie_chart', 'figure'),
    #             [Input('w_countries', 'value')])

    # def update_graph(w_countries):
    #     covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['total', 'death', 'recovered', 'active']].sum().reset_index()
    #     new_total = covid_data_2[covid_data_2['Country/Region'] == w_countries]['total'].iloc[-1]
    #     new_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-1]
    #     new_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1]
    #     new_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1]
    #     colors = ['orange', '#dd1e35', 'green', '#e55467']

    #     return {
    #         'data': [go.Pie(labels=['total', 'Death', 'Recovered', 'Active'],
    #                         values=[new_total, new_death, new_recovered, new_active],
    #                         marker=dict(colors=colors),
    #                         hoverinfo='label+value+percent',
    #                         textinfo='label+value',
    #                         textfont=dict(size=13),
    #                         hole=.7,
    #                         rotation=45
    #                         # insidetextorientation='radial',


    #                         )],

    #         'layout': go.Layout(
    #             # width=800,
    #             # height=520,
    #             plot_bgcolor='#1f2c56',
    #             paper_bgcolor='#1f2c56',
    #             hovermode='closest',
    #             title={
    #                 'text': 'Total Cases : ' + (w_countries),


    #                 'y': 0.93,
    #                 'x': 0.5,
    #                 'xanchor': 'center',
    #                 'yanchor': 'top'},
    #             titlefont={
    #                     'color': 'white',
    #                     'size': 20},
    #             legend={
    #                 'orientation': 'h',
    #                 'bgcolor': '#1f2c56',
    #                 'xanchor': 'center', 'x': 0.5, 'y': -0.07},
    #             font=dict(
    #                 family="sans-serif",
    #                 size=12,
    #                 color='white')
    #             ),


    #         }

    # # Create bar chart (show new cases)
    # @app.callback(Output('line_chart', 'figure'),
    #             [Input('w_countries', 'value')])
    # def update_graph(w_countries):
    # # main data frame
    #     covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['total', 'death', 'recovered', 'active']].sum().reset_index()
    # # daily total
    #     covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == w_countries][['Country/Region', 'date', 'total']].reset_index()
    #     covid_data_3['daily total'] = covid_data_3['total'] - covid_data_3['total'].shift(1)
    #     covid_data_3['Rolling Ave.'] = covid_data_3['daily total'].rolling(window=7).mean()

    #     return {
    #         'data': [go.Bar(x=covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30),
    #                         y=covid_data_3[covid_data_3['Country/Region'] == w_countries]['daily total'].tail(30),

    #                         name='Daily total',
    #                         marker=dict(
    #                             color='orange'),
    #                         hoverinfo='text',
    #                         hovertext=
    #                         '<b>Date</b>: ' + covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30).astype(str) + '<br>' +
    #                         '<b>Daily total</b>: ' + [f'{x:,.0f}' for x in covid_data_3[covid_data_3['Country/Region'] == w_countries]['daily total'].tail(30)] + '<br>' +
    #                         '<b>Country</b>: ' + covid_data_3[covid_data_3['Country/Region'] == w_countries]['Country/Region'].tail(30).astype(str) + '<br>'


    #                         ),
    #                 go.Scatter(x=covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30),
    #                             y=covid_data_3[covid_data_3['Country/Region'] == w_countries]['Rolling Ave.'].tail(30),
    #                             mode='lines',
    #                             name='Rolling average of the last seven days - daily total cases',
    #                             line=dict(width=3, color='#FF00FF'),
    #                             # marker=dict(
    #                             #     color='green'),
    #                             hoverinfo='text',
    #                             hovertext=
    #                             '<b>Date</b>: ' + covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30).astype(str) + '<br>' +
    #                             '<b>Rolling Ave.(last 7 days)</b>: ' + [f'{x:,.0f}' for x in covid_data_3[covid_data_3['Country/Region'] == w_countries]['Rolling Ave.'].tail(30)] + '<br>'
    #                             )],


    #         'layout': go.Layout(
    #             plot_bgcolor='#1f2c56',
    #             paper_bgcolor='#1f2c56',
    #             title={
    #                 'text': 'Last 30 Days total Cases : ' + (w_countries),
    #                 'y': 0.93,
    #                 'x': 0.5,
    #                 'xanchor': 'center',
    #                 'yanchor': 'top'},
    #             titlefont={
    #                         'color': 'white',
    #                         'size': 20},

    #             hovermode='x',
    #             margin = dict(r = 0),
    #             xaxis=dict(title='<b>Date</b>',
    #                         color='white',
    #                         showline=True,
    #                         showgrid=True,
    #                         showticklabels=True,
    #                         linecolor='white',
    #                         linewidth=2,
    #                         ticks='outside',
    #                         tickfont=dict(
    #                             family='Arial',
    #                             size=12,
    #                             color='white'
    #                         )

    #                 ),

    #             yaxis=dict(title='<b>Daily total Cases</b>',
    #                         color='white',
    #                         showline=True,
    #                         showgrid=True,
    #                         showticklabels=True,
    #                         linecolor='white',
    #                         linewidth=2,
    #                         ticks='outside',
    #                         tickfont=dict(
    #                         family='Arial',
    #                         size=12,
    #                         color='white'
    #                         )

    #                 ),

    #             legend={
    #                 'orientation': 'h',
    #                 'bgcolor': '#1f2c56',
    #                 'xanchor': 'center', 'x': 0.5, 'y': -0.3},
    #                         font=dict(
    #                             family="sans-serif",
    #                             size=12,
    #                             color='white'),

    #                 )

    #     }

    

    if __name__ == '__main__':
        app.run_server(debug=True)
