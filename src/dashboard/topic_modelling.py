from dash import html, dash_table
from styles import *
from dash import dcc

topic_modelling = html.Div(id="topic_modelling_container",
                           style=topic_modelling_container_style,
                           children=[
                               html.Iframe(id="my-iframe", src='assets/lda_vis.html',
                                           style={"width": "100%", "height": "100vh", "position": "flex",
                                                  "align-items": "center", "justify-content": "center",
                                                  "flex-direction": "column", "border": "none"})
                           ])
