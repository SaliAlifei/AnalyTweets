from dash import html
from src.dashboard.styles import *
from dash import dcc
import dash_leaflet as dl
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
from src.scripts.tweets import get_tweet_by_id, twitter_client_authentification
from src.scripts.preprocessing import preprocess, clean_texts
from src.scripts.models import nmf, get_n_top_words
from src.dashboard.nettoyage_donnees import get_current_df
from settings import NB_TOPICS, UNINTERRESTING_WORDS
from settings import ROOT_PATH


df = get_current_df()


def get_states():
    states_data = pd.read_csv(ROOT_PATH + "/data/statelatlong.csv")
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


def get_states_pie_chart():
    states_data = pd.read_csv(ROOT_PATH + "/data/statelatlong.csv")
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


def wordcloud(df, state="all", max_words=400, save=False):
    if state == "all":
        texts = df["cleaned_texts"].values
    else:
        texts = df[df["state"] == state]["cleaned_texts"].values

    # Suppression des mots qui ne sont pas interressants comme covid, coronavirus, etc
    texts = [' '.join([word for word in str(text).split() if word not in UNINTERRESTING_WORDS]) for text in texts]

    if len(texts) == 0:
        texts = ["NoEntry"]

    text = " ".join(str(review) for review in texts)
    wordcloud = WordCloud(width=650, height=300, background_color='#052140', max_words=max_words).generate(text)

    if save:
        # saving wordcloud as image
        wordcloud.to_file(ROOT_PATH + "/data/wordcloud-state.png")

    return wordcloud.to_image()


def get_topics_by_url(df, url):
    id = url.split("/")[-1]

    client = twitter_client_authentification()
    tweet = get_tweet_by_id(client, id)

    if tweet:
        # On charge le dataset
        df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]

        # On nettoie le texte du tweet et on l'ajoute à la liste
        tweet.append(clean_texts([tweet[1]])[0])

        # On ajoute le nouveau tweet à la fin du dataset
        tweet_index = df.shape[0]
        df.loc[tweet_index] = tweet

        # On lance le modèle
        topics = NB_TOPICS

        x, feature_names = preprocess(df['text'])
        nmf_model, w, h = nmf(x, topics)
        result = get_n_top_words(5, nmf_model, feature_names)

        # On recupère l'id du topic auquel appartient notre nouveau tweet
        id_topic_du_tweet = pd.DataFrame(w).loc[tweet_index].idxmax()

        # On cherche les 5 premiers mots definissant le mieux le topic
        top_5_mots = result[0][id_topic_du_tweet]
        return top_5_mots
    else:
        return "URL non valide"


analyse_exploratoire = html.Div(id="analyse_exploratoire_container",
                                style=analyse_exploratoire_container_style,
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
