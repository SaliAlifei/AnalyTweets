# Run this app with 'python dashboard_PPD.py' and
# visit http://127.0.0.1:8050/ in your web browser.

#
# Imports
#

#pip install plotly_express
import plotly_express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import get_data
import sentiment_analysis

#Number of Tweets (Total, Positive, Negative, Neutral)
def number_tweets(df):
    total_tweet = len(df)
    positive_tweet = len(df[df.TextBlob_Analysis=='Positive'])
    negative_tweet = len(df[df.TextBlob_Analysis=='Negative'])
    neutral_tweet = len(df[df.TextBlob_Analysis=='Neutral'])
    return (total_tweet,positive_tweet,negative_tweet,neutral_tweet)



if __name__ == '__main__':
    #
    # Data
    #
    
    #df = pd.read_csv('dataframe.csv')
    
    requete = "Covid-19 OR Covid OR Corona OR Pandémie OR épidémie OR Coronavirus OR virus"
    number=1000
    
    df_tweets = get_data.get_tweets(requete, number)
    df = sentiment_analysis.sentiment_analysis(df_tweets)
    
    total_tweet,positive_tweet,negative_tweet,neutral_tweet = number_tweets(df) 


    app = dash.Dash(__name__)
    
    fig = px.pie(df, names='TextBlob_Analysis', color_discrete_sequence=px.colors.sequential.RdBu)

    app.layout = html.Div(children=[
                            html.H1(children=f'Twitter sentiment analysis',
                                        style={'textAlign': 'center', 'color': 'brown'}),
                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ),
                             html.Div(children=f'Total number tweet    : {total_tweet}',
                                      style={'textAlign': 'center', 'color': '#7f7f7f'}), #d62728
                             
                             html.Div(children=f'Positive number tweet : {positive_tweet}',
                                      style={'textAlign': 'center', 'color': '#7f7f7f'}), #8c564b
                             
                             html.Div(children=f'Negative number tweet : {negative_tweet}',
                                      style={'textAlign': 'center', 'color': '#7f7f7f'}), 
                             
                             html.Div(children=f'Neutral number tweet  : {neutral_tweet}',
                                      style={'textAlign': 'center', 'color': '#7f7f7f'}) #tomato

    ])

    #
    # RUN APP
    #

    app.run_server(debug=True)
