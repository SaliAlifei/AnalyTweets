from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
from styles import *


df = pd.read_csv("../../data/data_map.csv")


def get_analyse_sentiments_df():
    return df


analyse_sentiments = html.Div(id="analyse_sentiments_container",
                              style=analyse_sentiments_container_style,
                              children=[
                                  html.Div(children=[
                                      html.Div(children=[
                                          dbc.RadioItems(
                                              id='my-radio-buttons',
                                              options=[
                                                  {"label": "Sentiments analysis", "value": "sentiment"},
                                                  {"label": "Topic model LDA", "value": "LDA"},
                                                  {"label": "Topic model NMF", "value": "NMF"},
                                              ],
                                              value="sentiment",
                                              inline=True,
                                              style={'margin-bottom': '70px', 'margin-left': '30px'}
                                          ),

                                          dcc.Graph(id="my-map"),

                                          dcc.Slider(0, 6,
                                                     step=None,
                                                     marks={
                                                         0: '2020',
                                                         1: 'janv 2020',
                                                         2: 'feb 2020',
                                                         3: 'mar 2020',
                                                         4: 'apr 2020',
                                                         5: 'may 2020',
                                                     },
                                                     value=0,
                                                     id='my-slider')

                                      ], style={'width': '49%', 'display': 'inline-block'}),

                                      html.Div(children=[
                                          html.Div(id='my-card', style={'margin-top': '20px'}),
                                          dcc.Graph(id="my-graph-bar2"),
                                      ], style={'width': '49%', 'display': 'inline-block'})
                                  ]),

                                  dcc.Graph(id="my-graph-bar")
                              ])
