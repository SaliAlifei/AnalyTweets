from dash import html
from src.dashboard.styles import *
from dash import dcc
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from src.dashboard.nettoyage_donnees import get_current_df
from settings import NB_TOPICS


def apply_nmf():
    documents = get_current_df()

    # TF IDF MATRIX
    # use tfidf by removing tokens that don't appear in at least 5 documents
    vect = TfidfVectorizer(min_df=5, stop_words='english')

    # Fit and transform
    X = vect.fit_transform(documents.cleaned_texts.astype("str"))
    # Use Gensim's NMF to get the best num of topics via coherence score
    # Create an NMF instance: model
    # the 10 components will be the topics
    model = NMF(n_components=NB_TOPICS, random_state=5)

    # Fit the model to TF-IDF
    model.fit(X)

    # Transform the TF-IDF: nmf_features
    nmf_features = model.transform(X)
    components_df = pd.DataFrame(model.components_, columns=vect.get_feature_names())

    topics = []

    for topic in range(components_df.shape[0]):
        tmp = components_df.iloc[topic]
        topics.append(tmp)

    for t in topics:
        wordcloud = WordCloud(background_color='white',
                              width=1500,
                              height=1000
                              ).generate_from_frequencies(t)
        # use .generate(space_separated_string) - to generate cloud from text

        plt.figure(figsize=(9, 6))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.savefig('assets/topic' + str(topic) + '.jpg')


imgs = []

for i in range(10):
    imgs.append(html.H1(children=f'Topic ' + str(i + 1), style={'textAlign': 'center', 'color': 'black'}))
    imgs.append(html.Img(src='assets/topic' + str(i) + '.jpg',
                         style={"width": "100%", "height": "100vh", "position": "flex", "align-items": "center",
                                "justify-content": "center", "flex-direction": "column", "border": "none"}))

topic_modelling = html.Div(id="topic_modelling_container",
                           style=topic_modelling_container_style,
                           children=[
                               html.Iframe(id="my-iframe", src='assets/lda_vis.html',
                                           style={"width": "100vw", "height": "100vh", "position": "flex",
                                                  "align-items": "center", "justify-content": "center",
                                                  "flex-direction": "column", "border": "none",
                                                  "margin-top": 10}),

                               dcc.Tabs([
                                   dcc.Tab(label='Topic modeling avec NMF', children=imgs),
                               ])
                           ])
