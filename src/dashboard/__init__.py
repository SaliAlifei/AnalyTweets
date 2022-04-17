import pandas as pd
from styles import *
import dash
from io import BytesIO
import base64
from analyse_exploratoire import *
from dash.dependencies import Input, Output, State
import dash_dangerously_set_inner_html
import re
from src.scripts.utils import wordcloud, get_topics_by_url
import requests

# App Layout
app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div(id="sidebar_container",
             style=sidebar_container_style,
             children=[
                 html.H1("AnalyTweets", id="title", style=title_style),
                 dcc.RadioItems(id="choose_model",
                                options=[
                                    {"label": "NMF", "value": "NMF"},
                                    {"label": "LDA", "value": "LDA"}],
                                value="NMF",
                                style=choose_model_style,
                                inputStyle=choose_model_input_style)
             ]),

    html.Div(id="content_container",
             style=content_container_style,
             children=[
                 analyse_exploratoire
             ])
], style=body_style)


@app.callback(
    Output('markers', 'children'),
    Input('map_dates_dropdown', 'value')
)
def update_map(value):
    if value is None:
        return get_map_markers(get_analyse_exploratoire_df())
    else:
        dataframe = select_df_by_date(get_dates(get_analyse_exploratoire_df(), unique=False), value)
        return get_map_markers(dataframe)


@app.callback(
    Output('wordcloud_img', 'src'),
    [Input('wordcloud_dropdown', 'value')]
)
def make_image(value):
    img = BytesIO()
    if value is None:
        wordcloud(get_analyse_exploratoire_df()).save(img, format='PNG')
        return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
    else:
        wordcloud(get_analyse_exploratoire_df(), state=value).save(img, format='PNG')
        return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


@app.callback(
    Output('tweet_topics_1', 'children'),
    Output('tweet_topics_2', 'children'),
    Output('tweet_topics_3', 'children'),
    Output('tweet_topics_4', 'children'),
    Output('tweet_topics_5', 'children'),
    [Input('analyze_button', 'n_clicks')],
    [State('analyze_tweet_url', 'value')])
def on_button_click(value, url):
    topics = get_topics_by_url(url)
    return [topic.capitalize() for topic in topics]


"""
@app.callback(
    Output('embed_tweet_div', 'children'),
    [Input('analyze_button', 'n_clicks')],
    [State('analyze_tweet_url', 'value')])
def embed_tweet(value, url):
    try:
        query_url = "https://publish.twitter.com/oembed?url=" + url
        payload = {'cards ': 'hidden',
                   'align ': 'center',
                   "hide_media": True,
                   "conversation": "none",
                   'width': 800}

        response = requests.get(query_url, params=payload).json()['html']

        #p, reste = response.split('dir="ltr">')[1].split("<a")
        #a_text = reste.split('">')[1].split("</a>")[0]
        #a_href = reste.split('href="')[1].split('">')[0]

        body = dash_dangerously_set_inner_html.DangerouslySetInnerHTML(response)
        print(body)

        output = html.Blockquote(id="embed_tweet",
                                 className="twitter-tweet",
                                 style={"height": 800, "width": 300, "data-cards": "hidden"},
                                 children=[
                                     body,
                                     dji.Import(src="https://platform.twitter.com/widgets.js")
                                 ])
        return output
    except Exception as e:
        print(e)
"""


if __name__ == "__main__":
    app.run_server(debug=True)
