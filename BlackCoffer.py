import dash
from dash import dcc
from dash import html
import json
import pandas as pd
import plotly.express as px
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from dash.dependencies import Input, Output
from pymongo import MongoClient
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Initialize the app
server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

#Read the File
df = pd.read_csv(r"C:\Users\Sylvester\Desktop\Blackcoffer Internship\result.csv")
df1 = df.fillna(method = "bfill")

#Build the components
Header_component = html.H1("Blackcoffer Assignment Dashboard", style = {'color' : 'purple'})


app.layout = html.Div([
    dbc.Row([
                Header_component
                 ]),
    dbc. Row([
        dbc.Col([
            dcc.Dropdown(id = "dpdn2",
                 value = ['Northern America', 'World'], multi= True,
                 placeholder = "Choose a Region...",
                 options = [{'label' : x, 'value' : x} for x in
                            df1.region.unique()])
        ]),
        dbc.Col([
            dcc.Dropdown(id="dpdn3",
                         value = [2016,2027], multi = True,
                         placeholder = "Select the Year...",
                         options = df1.end_year.unique())
        ])
        
        
    ]),
    html.Div([
        dcc.Graph(id = 'pie-graph', figure = {}, className = 'six columns'),
        dcc.Graph(id = 'area-graph', figure = {}, clickData = None, hoverData = None,
                  config = {
                      'staticPlot' : False,
                      'scrollZoom' : True,
                      'doubleClick' : 'reset',
                      'showTips' : True,
                      'displayModeBar' : True,
                      'watermark' : True,
                      #'modeBarButtonsToRemove' : ['pan2d', 'select2d'], 
                   },
                   className = 'six columns'
                   )
        
        
    ]),
    html.Div([dbc.Row([
        dbc.Col([
            dcc.Dropdown(id = "dpdn4",
                         value = ['gas', 'oil'], multi = True,
                         placeholder = "Choose a topic...",
                         options = df1.topic.unique())
        ]),
        dbc.Col([
            dcc.Dropdown(id = "dpdn5",
                         value = ["Energy", "Environment"], multi = True,
                         placeholder = "Sector....",
                         options = df1.sector.unique())
        ])
    ])
    ]),
    html.Div([
        dcc.Graph(id = 'bar-graph', figure = {}, className = "six columns")
    ]),
    html.Div([dbc.Row([
        dbc.Col([
            dcc.Dropdown(id = "dpdn6",
                         value = ["EIA", "SBWire"], multi = True,
                         placeholder = "Source......",
                         options = [{'label' : x, 'value' : x} for x in
                                    df1.source.unique()])
        ]),
        dbc.Col([
            dcc.Dropdown(id = "dpdn7",
                         value = ["Mexico", "Nigeria"], multi = True,
                         placeholder = "Choose a Country......",
                         options = df1.country.unique())
        ])
    ])
    ]),
    html.Div([
        dcc.Graph(id = 'scatter-plot', figure = {}, className = 'six columns')
    ])
])

@app.callback(
    Output(component_id = 'area-graph', component_property = 'figure'),
    Input(component_id = 'dpdn2', component_property = 'value'),
    Input(component_id = 'dpdn3', component_property = 'value'),
)

def update_graph(region_chosen, end_year_chosen):
    dfr = df1[df1.region.isin(region_chosen)]
    dfs = df1[df1.end_year.isin(end_year_chosen)]
    dff = [dfr,dfs]
    dff1 = pd.concat(dff)
    fig = px.area(data_frame = dff1, x = 'end_year', y = 'likelihood', color = 'region', line_group = 'country')
    return fig

@app.callback(
    Output(component_id = 'pie-graph', component_property = 'figure'),
    Input(component_id = 'dpdn2', component_property = 'value'),
    Input(component_id = 'dpdn3', component_property = 'value')
)

def update_pie_graph(region_chosen, end_year_chosen):
    dfr1 = df1[df1.region.isin(region_chosen)]
    dfs1 = df1[df1.end_year.isin(end_year_chosen)]
    dff2 = [dfr1,dfs1]
    dff21 = pd.concat(dff2)
    fig1 = px.pie(data_frame = dff21, values = 'end_year', names = 'region',
                  hover_data = 'topic',
                 title = "Topic Distribution in the Region")
    return fig1

@app.callback(
    Output(component_id = 'bar-graph', component_property = 'figure'),
    Input(component_id = 'dpdn4', component_property = 'value'),
    Input(component_id = 'dpdn5', component_property = 'value')
)

def update_bar_graph(topic_chosen, sector_chosen):
    dft = df1[df1.topic.isin(topic_chosen)]
    dfse = df1[df1.sector.isin(sector_chosen)]
    dff3 = [dft,dfse]
    dff31 = pd.concat(dff3)
    fig2 = px.bar(data_frame = dff31, x = 'region', y = 'topic', color = 'impact', animation_frame = 'start_year')
    return fig2

@app.callback(
    Output(component_id = 'scatter-plot', component_property = 'figure'),
    Input(component_id = 'dpdn6', component_property = 'value'),
    Input(component_id = 'dpdn7', component_property = 'value')
)

def update_scatter_plot(source_chosen, country_chosen):
    dfsc = df1[df1.source.isin(source_chosen)]
    dfcou = df1[df1.country.isin(country_chosen)]
    dff4 = [dfsc, dfcou]
    dff41 = pd.concat(dff4)
    #return scatter plot figure here
    fig3 = px.scatter(data_frame = dff41, x = 'country', y = 'source', color = 'relevance', animation_frame = 'end_year')
    return fig3
        
        









app.run_server(debug = True)