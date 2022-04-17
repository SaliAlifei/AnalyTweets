from dash import html
from styles import *
from dash import dcc
import pandas as pd
import dash_leaflet as dl
import plotly.graph_objs as go
import plotly.express as px
import dash_defer_js_import as dji

df = pd.read_csv("../../data/resultats_shuflled_0_a_300.csv")


def get_states():
    states_data = pd.read_csv("../../data/statelatlong.csv")
    states = states_data['City']
    states_ab = states_data['state']
    return list(zip(states, states_ab))


def get_dates(df, unique=True):
    # On cherche à obtenir un format "Mois AAAA"
    dates = pd.to_datetime(df['created_at']).dt.strftime("%B %Y")
    if unique:
        return pd.unique(dates)
    else:
        return dates


def select_df_by_date(dates, selection_date):
    # selection_date = "May 2020" par exemple
    dataframe = df.loc[dates[dates == selection_date].index]
    return dataframe


def select_df_by_state(state):
    return df.loc[df['state'] == state]


def get_map_markers(df):
    # lat_lon = [list(x) for x in list(zip(df['latitude'], df['longitude']))]

    markers = []

    for index, row in df.iterrows():
        text = row['text']
        lat = row['latitude']
        lon = row['longitude']
        markers.append(
            dl.Marker(
                title=text,
                position=(lat, lon),
                children=[
                    dl.Tooltip(text),
                    dl.Popup(text),
                ]
            )
        )
    return markers


def get_analyse_exploratoire_df():
    return df


def get_states_pie_chart():
    states_data = pd.read_csv("../../data/statelatlong.csv")
    states = states_data['state']

    df_state = df['state'].value_counts()

    counts = []
    for state in states:
        if state in df_state:
            counts.append(df_state[state])
        else:
            counts.append(0)

    data = list(zip(states, counts))
    sorted_data = sorted(data, key=lambda tup: tup[1], reverse=True)[:10]

    states, counts = zip(*sorted_data)

    fig = px.pie(values=counts, names=states, title='Nombre de tweets par Etat')

    fig.update_layout(
        paper_bgcolor='#2f5972',
        plot_bgcolor='red',
        font=dict(color="white"),
        width=550, height=330,
        margin=go.layout.Margin(l=0, r=0, b=0, t=70, pad=4)
    )
    return fig


analyse_exploratoire = html.Div(id="analyse_exploratoire_container",
                                children=[
                                    html.Div(id="map_container",
                                             style=map_container_style,
                                             children=[
                                                 dcc.Dropdown(
                                                     id='map_dates_dropdown',
                                                     style=map_dates_dropdown_style,
                                                     options=[
                                                         {'label': i, 'value': i} for i in get_dates(df, unique=True)
                                                     ]),

                                                 dl.Map([dl.TileLayer(),
                                                         dl.MarkerClusterGroup(id="markers",
                                                                               children=get_map_markers(df))
                                                         ],
                                                        id="map",
                                                        center=[39, -98],
                                                        zoom=5,
                                                        zoomControl=False,
                                                        style={'width': '100%', 'height': '100%'})
                                             ]),

                                    html.Div(id="chart_container",
                                             style=chart_container_style,
                                             children=[
                                                 html.Div(id="wordcloud_container",
                                                          style=wordcloud_container_style,
                                                          children=[
                                                              dcc.Dropdown(
                                                                  id='wordcloud_dropdown',
                                                                  style=wordcloud_dropdown_style,
                                                                  options=[
                                                                      {'label': i, 'value': j} for i, j in get_states()
                                                                  ],
                                                              ),

                                                              html.Img(id="wordcloud_img"),
                                                          ]),

                                                 html.Div(id="pie_container",
                                                          style=pie_container_style,
                                                          children=[
                                                              dcc.Graph(id="pie_chart", figure=get_states_pie_chart(),
                                                                        style={"margin": 0, "padding": 0,
                                                                               "background-color": "#2f5972"})
                                                          ])
                                             ]),

                                    html.Div(id="analyze_tweet_container",
                                             style=analyze_tweet_container_style,
                                             children=[
                                                 html.Div(id="analyze_container",
                                                          style=analyze_container_style,
                                                          children=[
                                                              dcc.Input(id="analyze_tweet_url",
                                                                        style=analyze_tweet_url_style,
                                                                        value="https://twitter.com/JulieKaplow/status/1515405110096060422"),

                                                              html.Button("Analyze",
                                                                          id="analyze_button",
                                                                          style=analyze_button_style)
                                                          ]),

                                                 # html.Div(id="embed_tweet_div", children=[]),

                                                 html.Div(id="results_container",
                                                          style=results_container_style,
                                                          children=[
                                                              html.Div(id='tweet_topics_1',
                                                                       style=topics_div_style),
                                                              html.Div(id='tweet_topics_2',
                                                                       style=topics_div_style),
                                                              html.Div(id='tweet_topics_3',
                                                                       style=topics_div_style),
                                                              html.Div(id='tweet_topics_4',
                                                                       style=topics_div_style),
                                                              html.Div(id='tweet_topics_5',
                                                                       style=topics_div_style)
                                                          ])
                                             ]),
                                ])

if __name__ == "__main__":
    state = "AZ"
    select_df_by_state(state)
