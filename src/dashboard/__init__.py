import dash
from dash.dependencies import Input, Output, State

import re
import string
import contractions
from io import BytesIO
import base64

from analyse_exploratoire import *
from nettoyage_donnees import *
from analyse_sentiments import *
from topic_modelling import *
from styles import *

import gensim
import gensim.corpora as corpora
import pyLDAvis
import pyLDAvis.gensim_models

from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# App Layout
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Accueil',
                style=tab_style,
                selected_style=selected_tab_style,
                children=[
                    analyse_exploratoire
                ]),

        dcc.Tab(label='Nettoyage des données',
                style=tab_style,
                selected_style=selected_tab_style,
                children=[
                    nettoyage_donnees
                ]),

        dcc.Tab(label='Analyse spatio-temporelle',
                style=tab_style,
                selected_style=selected_tab_style,
                children=[
                    analyse_sentiments
                ]),

        dcc.Tab(label='Topic modeling',
                style=tab_style,
                selected_style=topic_modelling_selected_tab_style,
                children=[
                    topic_modelling
                ])
    ])
], style=body_style)


# --------------------------------------------------------------------------------------
# ----------------------------- Analyse Exploratoire Tab -------------------------------
# --------------------------------------------------------------------------------------

@app.callback(
    Output('markers', 'children'),
    Input('map_dates_dropdown', 'value')
)
def update_map(value):
    if value is None:
        return get_map_markers(get_current_df())
    else:
        dataframe = select_df_by_date(get_dates(get_current_df(), unique=False), value)
        return get_map_markers(dataframe)


@app.callback(
    Output('wordcloud_img', 'src'),
    [Input('wordcloud_dropdown', 'value')]
)
def make_image(value):
    img = BytesIO()
    if value is None:
        wordcloud(get_current_df()).save(img, format='PNG')
        return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
    else:
        wordcloud(get_current_df(), state=value).save(img, format='PNG')
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
    topics = get_topics_by_url(get_current_df(), url)
    return [topic.capitalize() for topic in topics]


# --------------------------------------------------------------------------------------
# ----------------------------- Nettoyage des données Tab ------------------------------
# --------------------------------------------------------------------------------------


@app.callback(
    Output('my-checklist', 'value'),
    Output('my-table', 'data'),
    Output('my-table', 'columns'),
    Input('my-checklist', 'value'),
)
def clean_data(techniques_selected):
    # On charge le df de base
    df = pd.read_csv("../../data/original_df.csv").loc[:1000].copy()

    if 'links' in techniques_selected:
        df["text"] = df["text"].apply(lambda x: re.sub(r"http\S+", "", x))
        df["text"] = df["text"].apply(lambda x: re.sub(r"www.\S+", "", x))

    if 'lowercase' in techniques_selected:
        df["text"] = df["text"].apply(lambda x: x.lower())

    if 'punctuations' in techniques_selected:
        a = string.punctuation.replace('#', '')
        b = a.replace('@', '')
        df["text"] = df["text"].apply(lambda x: re.sub(r'[{}]'.format(b), "", x))

    if 'hashtags' in techniques_selected:
        df["text"] = df["text"].apply(lambda x: re.sub("#", "", x))

    if 'mentions' in techniques_selected:
        df["text"] = df["text"].apply(lambda x: re.sub("@", "", x))

    if 'emojis' in techniques_selected:
        regex_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", re.UNICODE)
        df["text"] = df["text"].apply(lambda x: regex_pattern.sub(r'', x))

    if 'stemming' in techniques_selected:
        df["text"] = df["text"].apply(lambda x: ' '.join([stemmer.stem(word) for word in word_tokenize(x)]))

    if 'lemmatization' in techniques_selected:
        df["text"] = df["text"].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(x)]))

    if 'stop word' in techniques_selected:
        df["text"] = df["text"].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

    if 'contractions' in techniques_selected:
        df["text"] = df["text"].apply(lambda x: ' '.join([contractions.fix(word) for word in x.split()]))

    if 'few words' in techniques_selected:
        df = df[df['text'].str.split().str.len() > 3]

    # On remplace le df current par le nouveau après avoir appliqué les modifications
    df.loc[:, "cleaned_texts"] = df["text"]
    df.to_csv("../../data/current_df.csv")

    data = df.to_dict('records')

    columns = [{"name": i, "id": i} for i in ['index', 'text']]

    return techniques_selected, data, columns


# --------------------------------------------------------------------------------------
# ---------------------------- Analyse des sentiments Tab ------------------------------
# --------------------------------------------------------------------------------------


@app.callback(
    Output("my-map", "figure"),
    Input("my-radio-buttons", "value"),
    Input('my-slider', 'value'))
def display_map(radio_button_value, slider_value):
    df = get_analyse_sentiments_df()

    if radio_button_value == 'LDA':
        colorbar_title = "LDA topics"
        data_type = str
    elif radio_button_value == 'NMF':
        colorbar_title = "NMF topics"
        data_type = str
    else:
        colorbar_title = "Sentiments"
        data_type = float

    fig = px.choropleth(
        locations=df['state'].loc[df['month'] == slider_value],
        locationmode="USA-states",
        color=df[radio_button_value].loc[df['month'] == slider_value].astype(data_type),
        color_continuous_scale=["red", "yellow", "green"],
        color_discrete_sequence=px.colors.qualitative.G10,
        scope="usa",
    )

    fig.update_layout(
        paper_bgcolor='#2f5972',
        font=dict(color="white"),
        title_text=colorbar_title + ' by states',
        geo_scope='usa',
        coloraxis_colorbar_title_text=colorbar_title,
    )

    return fig


@app.callback(
    Output('my-card', 'children'),
    Input("my-map", "hoverData"),
    Input('my-slider', 'value'))
def update_kpi_card(hoover_text, slider_value):
    df = get_analyse_sentiments_df()
    text = 'USA'
    value = df['Total'].loc[(df['state'] == 'USA') & (df['month'] == slider_value)]

    if (hoover_text):
        state_selected = hoover_text['points'][0]['location']
        text = df['state_name'].loc[(df['state'] == state_selected) & (df['month'] == slider_value)]
        value = df['Total'].loc[(df['state'] == state_selected) & (df['month'] == slider_value)]

    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(text),
                    html.P(value)
                ]
            ),
        ],
        style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '40%', 'text-align': 'center'},
    )

    return card


@app.callback(
    Output("my-graph-bar2", "figure"),
    Input("my-map", "hoverData"),
    Input('my-slider', 'value'))
def update_bar_chart_words(hoover_text, slider_value):
    words = df['words'].loc[(df['state'] == 'USA') & (df['month'] == slider_value)].values[0]
    freq = df['freq'].loc[(df['state'] == 'USA') & (df['month'] == slider_value)].values[0]

    if hoover_text:
        state_selected = hoover_text['points'][0]['location']
        words = df['words'].loc[(df['state'] == state_selected) & (df['month'] == slider_value)].values[0]
        freq = df['freq'].loc[(df['state'] == state_selected) & (df['month'] == slider_value)].values[0]

    # nettoyer les listes
    words = re.sub('\n', '', words)
    words = re.sub("'", '', words)
    words = words.strip('][').split(' ')

    freq = re.sub('\n', '', freq)
    freq = re.sub('\s+', ' ', freq)
    freq = re.sub('\s+]', '', freq)
    freq = freq.strip('][').split(' ')
    freq = [int(i) for i in freq]

    fig = go.Figure(data=[
        go.Bar(x=freq[::-1], y=words[::-1], orientation='h'),
    ])

    fig.update_layout(
        paper_bgcolor='#2f5972',
        font=dict(color="white"),
        title_text='Top words')

    return fig


@app.callback(
    Output("my-graph-bar", "figure"),
    Input("my-radio-buttons", "value"),
    Input("my-map", "hoverData"),
    Input('my-slider', 'value'))
def update_bar_chart(radio_button_value, hoover_text, slider_value):
    if radio_button_value == 'LDA':
        columns = ['LDA_0', 'LDA_1', 'LDA_2', 'LDA_3', 'LDA_4', 'LDA_5', 'LDA_6', 'LDA_7', 'LDA_8', 'LDA_9', ]
    elif radio_button_value == 'NMF':
        columns = ['NMF_0', 'NMF_1', 'NMF_2', 'NMF_3', 'NMF_4', 'NMF_5', 'NMF_6', 'NMF_7', 'NMF_8', 'NMF_9', ]
    else:
        columns = ['Negative', 'Neutral', 'Positive']

    row = df[columns].loc[(df['state'] == 'USA') & (df['month'] == slider_value)].values[0]

    if (hoover_text):
        state_selected = hoover_text['points'][0]['location']
        row = df[columns].loc[(df['state'] == state_selected) & (df['month'] == slider_value)].values[0]

    fig = go.Figure(data=[
        go.Bar(x=columns, y=row),
    ])

    fig.update_layout(
        paper_bgcolor='#2f5972',
        font=dict(color="white"),
        title_text='Repartition')

    return fig


# --------------------------------------------------------------------------------------
# -------------------------------- Topic Modelling Tab ---------------------------------
# --------------------------------------------------------------------------------------

@app.callback(
    Output('my-iframe', 'src'),
    Input('my-table','data'),
    Input('my-button-lda', 'n_clicks'),
)
def apply_lda(data, n_clicks):

    if n_clicks != 0 :

        df = pd.DataFrame(data)

        def sent_to_words(sentences):
            for sentence in sentences:
                # deacc=True removes punctuations
                yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

        data_sent = df["text"].values.tolist()
        data_words = list(sent_to_words(data_sent))

        # Create Dictionary
        id2word = corpora.Dictionary(data_words)
        # Create Corpus
        texts = data_words
        # Term Document Frequency
        corpus = [id2word.doc2bow(text) for text in texts]
        # LDA model training
        from pprint import pprint
        # number of topics
        num_topics = 10
        # Build LDA model
        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                               id2word=id2word,
                                               num_topics=num_topics)

        vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word)
        pyLDAvis.save_html(vis, 'assets/lda_vis.html')


    return 'assets/lda_vis.html'



if __name__ == "__main__":
    app.run_server(debug=True)
