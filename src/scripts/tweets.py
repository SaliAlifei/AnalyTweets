import os
import pandas as pd
import tweepy
from settings import load_env

load_env()

api_key = os.environ.get("TWITTER_API_KEY")
api_secret_key = os.environ.get("TWITTER_API_SECRET_KEY")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")


INTERRESTING_COLUMNS = ['id', "text", "lang", "created_at"]


def twitter_client_authentification():
    client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_secret_key,
                           access_token=access_token, access_token_secret=access_token_secret)
    return client


def get_tweet_by_id(client, tweet_id):
    data = client.get_tweet(tweet_id, tweet_fields=INTERRESTING_COLUMNS).data
    if data is None:
        print(f"Le tweet avec l'id = {tweet_id} n'existe pas")
        return False
    else:
        tweet = []
        for col in INTERRESTING_COLUMNS:
            tweet.append(data[col])
    return tweet


def get_tweets_by_id(client, list_id):
    tweets = client.get_tweets(list_id, tweet_fields=INTERRESTING_COLUMNS).data
    if tweets is None:
        print("Aucun des tweets avec les id marqués n'existent")
        return False

    # Transformation des objets 'Tweet' en liste [id, text]
    structured_tweets = []
    for tweet in tweets:
        one_tweet = []
        for col in INTERRESTING_COLUMNS:
            one_tweet.append(tweet[col])
        structured_tweets.append(one_tweet)

    return pd.DataFrame(structured_tweets, columns=INTERRESTING_COLUMNS)


def response_to_dataframe(response):
    structured_tweets = []
    for tweet in response.data:
        structured_tweets.append([tweet['id'], tweet['text'], tweet['lang'], tweet['created_at']])
    return pd.DataFrame(structured_tweets, columns=INTERRESTING_COLUMNS)


def search_tweets(client, termes_a_rechercher, tweet_fields, max_results=10, save_result=True):
    # Filtres pour la recherche
    no_media = " -has:media"
    no_retweet = " -is:retweet"
    in_english = " lang:en"

    query = termes_a_rechercher + no_media + no_retweet + in_english
    reponse = client.search_recent_tweets(query=query,  max_results=max_results, tweet_fields=tweet_fields)

    df = response_to_dataframe(reponse)

    if save_result:
        df.to_csv(f"recherche_{termes_a_rechercher}.csv")

    return df


if __name__ == "__main__":

    twitter_client = twitter_client_authentification()
    response = search_tweets(twitter_client, "covid", tweet_fields=INTERRESTING_COLUMNS)
    print(response)
