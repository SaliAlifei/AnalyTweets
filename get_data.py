# Import #


import pandas as pd
from tweepy import OAuthHandler
import tweepy


#Connexion API Twitter

#Your credentials to access Twitter API 
consumer_key = 'SP3rKT4WnTbWNAF2mmnnmvtwS'
consumer_secret = '35gK0RLzOKzQgplRHtkGztysMpSpFSAFL1PJPksJOnVeBDSI5u'
access_token = '1502685387361247233-MuYJFNQb38jOTyHiExekQxeQnr1NnR'
access_token_secret = 'Nrlyqhiz80a4zDxmIUqXeKZKVv2TgPbA622gi95z64xZH'

#Twitter authentication and the connection to Twitter Streaming API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


# requete = "Covid-19 OR Covid OR Corona OR Pandémie OR épidémie OR Coronavirus OR virus"
#since='2021-05-01'
#number=1000

def get_tweets(requete, number):
    '''

    Parameters
    ----------
    requete : STR
        keywords of the tweets.
    date : TYPE
        date of extract beginning.
    number : INT
        number of tweets to extract.

    Returns
    -------
    df_tweets : DATAFRAME
        dataframe of tweets.

    '''
    requete = requete
    
    tweets = tweepy.Cursor(api.search_tweets,
                       q = requete,
                       lang = "en").items(number)
    
    all_tweets = [tweet.text for tweet in tweets]

    df_tweets = pd.DataFrame(all_tweets, columns=['tweet'])
    
    return df_tweets
