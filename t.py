# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from asyncio.windows_events import NULL
from dash import Dash, dcc, html, Input, Output, State, callback_context, dash_table
import pandas as pd
import re
import string
import contractions
import plotly_express as px
from textblob import TextBlob

#import nltk
#nltk.download()

from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
lemmatizer = WordNetLemmatizer()

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

df_csv = pd.read_csv('data.csv')


app = Dash(__name__)


app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Accueil', children=[

        ]),



        dcc.Tab(label='Nettoyage des données', children=[
            html.Div([

                html.Div(children=[

                    html.H2(children='Data cleaning'),

                    html.Label('Preprocessing techniques :'),
                    dcc.Checklist(['links', 'lowercase', 'punctuations', 'hashtags', 'mentions', 'emojis', 'stemming', 'lemmatization', 'stop word', 'contractions', 'few words'],
                                ['links', 'lowercase'],
                                id="my-checklist",
                                labelStyle={'display': 'block'},
                    ),

                    html.Button('Sentiments analysis', id='my-button-sentiments', n_clicks=0),
                    html.Button('Topic modeling', id='my-button-lda', n_clicks=0),

                ], style={'padding': 10, 'flex': 0.15}),

                html.Div(children=[    
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
                ], style={'padding': 10, 'flex': 1}),
                
            ], style={'display': 'flex', 'flex-direction': 'row'})
        ]),

        dcc.Tab(label='Analyse des sentiments', children=[
                            html.H1(children=f'Twitter sentiment analysis',
                                        style={'textAlign': 'center', 'color': 'brown'}),
                            dcc.Graph(
                                id='my-graph', 
                            ),
                             html.Div(children=['Total number tweets    : ', html.Span(id='my-total-tweets', children='')],
                                      style={'textAlign': 'center', 'color': '#7f7f7f'}), #d62728
                             
                             html.Div(children=['Positive number tweets : ', html.Span(id='my-positive-tweets', children='')],
                                      style={'textAlign': 'center', 'color': '#7f7f7f'}), #8c564b
                             
                             html.Div(children=['Negative number tweets : ', html.Span(id='my-negative-tweets', children='')],
                                      style={'textAlign': 'center', 'color': '#7f7f7f'}), 
                             
                             html.Div(children=['Neutral number tweets  : ', html.Span(id='my-neutral-tweets', children='')],
                                      style={'textAlign': 'center', 'color': '#7f7f7f'}) #tomato
        ]),

        dcc.Tab(label='Topic modeling', children=[
            html.Iframe(id="my-iframe", src='assets/lda_vis.html',
            style={"width": "100%", "height": "100vh", "position": "flex", "align-items": "center", "justify-content": "center", "flex-direction": "column", "border": "none"})
        ]),
    ])
])

@app.callback(
    Output('my-checklist', 'value'),
    Output('my-table','data'),
    Output('my-table','columns'),
    Input('my-checklist', 'value'),
)
def clean_data(techniques_selected):

    df = df_csv.copy()

    if 'links' in techniques_selected:
        df["text"] = df["text"].apply(lambda x : re.sub(r"http\S+", "", x))
        df["text"] = df["text"].apply(lambda x : re.sub(r"www.\S+", "", x))

    if 'lowercase' in techniques_selected:    
        df["text"] = df["text"].apply(lambda x : x.lower())

    if 'punctuations' in techniques_selected:    
        a = string.punctuation.replace('#','')
        b = a.replace('@','')
        df["text"] = df["text"].apply(lambda x : re.sub(r'[{}]'.format(b),"", x))

    if 'hashtags' in techniques_selected:
        df["text"] = df["text"].apply(lambda x : re.sub("#","", x))

    if 'mentions' in techniques_selected:
        df["text"] = df["text"].apply(lambda x : re.sub("@","", x))

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
        df["text"] = df["text"].apply(lambda x : regex_pattern.sub(r'',x))

    if 'stemming' in techniques_selected:
        df["text"] = df["text"].apply(lambda x : ' '.join([stemmer.stem(word) for word in word_tokenize(x)]))

    if 'lemmatization' in techniques_selected:
        df["text"] = df["text"].apply(lambda x : ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(x)]))

    if 'stop word' in techniques_selected:
        df["text"] = df["text"].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

    if 'contractions' in techniques_selected:
        df["text"] = df["text"].apply(lambda x: ' '.join([contractions.fix(word) for word in x.split()]))

    if 'few words' in techniques_selected:
        df = df[df['text'].str.split().str.len() > 3]

    data = df.to_dict('records')

    columns = [{"name": i, "id": i} for i in ['index', 'text']]

    return techniques_selected, data, columns


@app.callback(
    Output('my-graph', 'figure'),
    Output('my-total-tweets', 'children'),
    Output('my-positive-tweets', 'children'),
    Output('my-negative-tweets', 'children'),
    Output('my-neutral-tweets', 'children'),    
    Input('my-table','data'),
    Input('my-button-sentiments', 'n_clicks'),
)
def apply_sentiments_analysis(data, n_clicks):

    def sentiment_analysis(tweet):
        '''
        Parameters
        ----------
        tweet : DATAFRAME
            dataframe of tweets.
        Returns
        -------
        DATAFRAME
            dataframe of tweets with a sentiment analysis of each tweet.
        '''
        #function to get the subjectivity
        def getSubjectivity(text):
            return TextBlob(text).sentiment.subjectivity

        #function to get the polarity
        def getPolarity(text):
            return TextBlob(text).sentiment.polarity

        #Create two new columns ‘Subjectivity’ & ‘Polarity’
        tweet['TextBlob_Subjectivity'] = tweet['text'].apply(getSubjectivity)
        tweet['TextBlob_Polarity'] = tweet['text'].apply(getPolarity)

        def getAnalysis(score):
            if score < 0 :
                return 'Negative'

            elif score == 0 :
                return 'Neutral'

            else :
                return 'Positive'

        tweet['TextBlob_Analysis'] = tweet['TextBlob_Polarity'].apply(getAnalysis)

        return tweet

    #Number of Tweets (Total, Positive, Negative, Neutral)
    def number_tweets(df):
        total_tweet = len(df)
        positive_tweet = len(df[df.TextBlob_Analysis=='Positive'])
        negative_tweet = len(df[df.TextBlob_Analysis=='Negative'])
        neutral_tweet = len(df[df.TextBlob_Analysis=='Neutral'])
        return (total_tweet,positive_tweet,negative_tweet,neutral_tweet)

    if n_clicks != -1 :

        df = pd.DataFrame(data)
        
        df_sent = sentiment_analysis(df)

        total_tweet,positive_tweet,negative_tweet,neutral_tweet = number_tweets(df) 

        fig = px.pie(df_sent, names='TextBlob_Analysis', color_discrete_sequence=px.colors.sequential.RdBu)
    
    print(n_clicks)

    return fig, total_tweet, positive_tweet, negative_tweet, neutral_tweet



@app.callback(
    Output('my-iframe', 'src'),
    Input('my-table','data'),
    Input('my-button-lda', 'n_clicks'),
)
def apply_lda(data, n_clicks):

    if n_clicks != 0 :

        df = pd.DataFrame(data)

        import gensim
        from gensim.utils import simple_preprocess
        def sent_to_words(sentences):
            for sentence in sentences:
                # deacc=True removes punctuations
                yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
        data_sent = df["text"].values.tolist()
        data_words = list(sent_to_words(data_sent))
        import gensim.corpora as corpora
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
        doc_lda = lda_model[corpus]
        import pyLDAvis
        import pyLDAvis.gensim_models
        vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word)
        pyLDAvis.save_html(vis, 'assets/lda_vis.html')

    return 'assets/lda_vis.html'

if __name__ == '__main__':
    app.run_server(debug=True)

