from dash import html, dash_table
from styles import *
from dash import dcc
import pandas as pd


df = pd.read_csv("../../data/current_df.csv").loc[:1000]


def get_current_df():
    return df


nettoyage_donnees = html.Div(id="nettoyage_donnees_container",
                             style=nettoyage_donnees_container_style,
                             children=[
                                 html.Div(id="nettoyage_donnees_sidebar",
                                          style=nettoyage_donnees_sidebar_style,
                                          children=[
                                              html.H2(children='Data cleaning',
                                                      style=nettoyage_donnees_title_style),

                                              html.Label('Preprocessing techniques :',
                                                         style=nettoyage_donnees_subtitle_style),

                                              dcc.Checklist(
                                                  ['links', 'lowercase', 'punctuations', 'hashtags', 'mentions',
                                                   'emojis', 'stemming', 'lemmatization', 'stop word', 'contractions',
                                                   'few words'],
                                                  ['links', 'lowercase'],
                                                  id="my-checklist",
                                                  style=nettoyage_donnees_checklist_style,
                                                  labelStyle={'display': 'block'},
                                                  inputStyle={"margin-right": "5px"},
                                                  persistence=True,
                                                  persistence_type='session'
                                              )
                                          ]),

                                 html.Div(id="nettoyage_donnees_table",
                                          style=nettoyage_donnees_table_style,
                                          children=[
                                              dash_table.DataTable(
                                                  id='my-table',
                                                  data=[],
                                                  page_size=15,
                                                  style_data={
                                                      'whiteSpace': 'normal',
                                                      'height': 'auto',
                                                  },
                                                  style_cell={'textAlign': 'left'},
                                                  style_as_list_view=True
                                              )
                                          ]),

                             ])
