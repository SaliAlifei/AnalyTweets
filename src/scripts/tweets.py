import os
import random

import numpy as np
import pandas as pd
from random import randint
import tweepy
from settings import load_env
from TwitterAPI import TwitterAPI

load_env()

api_key = os.environ.get("TWITTER_API_KEY")
api_secret_key = os.environ.get("TWITTER_API_SECRET_KEY")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

INTERRESTING_COLUMNS = ['id', "text", "lang", "created_at", "geo"]
DATASET_COLUMNS = ['id', "text", "lang", "created_at", "geo", "state", "city" 'longitude', 'latitude']
TOPICS = ["covid", "cooking", "sports", "war", "politics", "journalism", "movie", "technology", "music", "beauty"]


def twitter_client_authentification():
    client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_secret_key,
                           access_token=access_token, access_token_secret=access_token_secret, wait_on_rate_limit=True)
    return client


def get_tweet_by_id_twitterapi(id):
    api = TwitterAPI(api_key, api_secret_key, access_token, access_token_secret, api_version='2')
    r = api.request(f'tweets/:{id}', {'tweet.fields': "id,text,lang,created_at,geo",
                                      'expansions': 'geo.place_id',
                                      'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type'})

    for item in r:
        print(item)

    print(r.get_quota())


def get_tweet_by_id(client, tweet_id, with_geo=True):
    if with_geo:
        retrieved_tweet = client.get_tweet(tweet_id, tweet_fields=INTERRESTING_COLUMNS,
                                           place_fields=['country', 'country_code', 'full_name', 'geo', 'id', 'name',
                                                         'place_type'],
                                           expansions="geo.place_id")
    else:
        retrieved_tweet = client.get_tweet(tweet_id, tweet_fields=INTERRESTING_COLUMNS)

    data = retrieved_tweet.data

    if data is None:
        print(f"Le tweet avec l'id = {tweet_id} n'existe pas")
        return False
    else:
        tweet = []
        for col in INTERRESTING_COLUMNS:
            tweet.append(data[col])

        if with_geo:
            state, city, latitude, longitude = ["NA", "NA", 0, 0]
            try:
                place = retrieved_tweet.includes['places'][0]
                bbox = place['geo']['bbox']
                city, state = place['full_name'].split(", ")
                latitude = bbox[1]
                longitude = bbox[0]
            except Exception as e:
                print(e)

            tweet.append(state)
            tweet.append(city)
            tweet.append(longitude)
            tweet.append(latitude)

    return tweet


def get_tweets_by_id_with_geo(client, list_id):
    retrieved_tweets = client.get_tweets(list_id, tweet_fields=INTERRESTING_COLUMNS,
                                         place_fields=['country', 'country_code', 'full_name', 'geo', 'id', 'name',
                                                       'place_type'],
                                         expansions="geo.place_id")
    data = retrieved_tweets.data
    tweet_includes = retrieved_tweets.includes['places']

    if len(data) == 0:
        print(f"Aucun des tweets de la liste donnée n'existe")

    # Extract list of place_id from tweets data
    data_place_ids = [tweet['geo']['place_id'] if tweet['geo'] else "nothing" for tweet in data]

    # Extract place_id from data includes
    include_place_ids = [place['id'] for place in retrieved_tweets.includes['places']]

    tweets = []
    for i in range(len(data)):
        tweet_data = data[i]
        if data_place_ids[i] == "nothing":
            state, city, latitude, longitude = ["NA", "NA", 0, 0]
        elif data_place_ids[i] in include_place_ids:
            include_id = include_place_ids.index(data_place_ids[i])
            place = tweet_includes[include_id]
            bbox = place['geo']['bbox']
            city = place['full_name'].split(", ")[0]
            state = place['full_name'].split(", ")[1]
            latitude = bbox[1]
            longitude = bbox[0]
        else:
            state, city, latitude, longitude = ["NA", "NA", 0, 0]

        tweet = []
        for col in INTERRESTING_COLUMNS:
            tweet.append(tweet_data[col])

        tweet.append(state)
        tweet.append(city)
        tweet.append(longitude)
        tweet.append(latitude)

        tweets.append(tweet)

    return pd.DataFrame(tweets, columns=DATASET_COLUMNS)


def get_tweets_by_id(client, list_id, with_geo=True):
    f = open("../../data/resultats/not_found_ids.txt", "a")

    tweets = []
    for id in list_id:
        tweet = get_tweet_by_id(client, id, with_geo=with_geo)
        if tweet:
            tweets.append(tweet)
        else:
            f.write(id + "\n")

    f.close()

    if with_geo:
        return pd.DataFrame(tweets, columns=DATASET_COLUMNS)
    else:
        return pd.DataFrame(tweets, columns=INTERRESTING_COLUMNS)


def response_to_dataframe(response):
    structured_tweets = []
    for tweet in response.data:
        structured_tweets.append([tweet['id'], tweet['text'], tweet['lang'], tweet['created_at']])
    return pd.DataFrame(structured_tweets, columns=INTERRESTING_COLUMNS)


def search_tweets(client, termes_a_rechercher, tweet_fields, max_results=10, save_result=True):
    # Filtres pour la recherche
    no_media = " -has:media"
    no_retweet = " -is:retweet"
    no_reply = " -is:reply"
    no_link = " -has:links"
    in_english = " lang:en"

    query = termes_a_rechercher + no_media + no_retweet + no_reply + no_link + in_english
    reponse = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=tweet_fields)

    df = response_to_dataframe(reponse)

    if save_result:
        df.to_csv(f"recherche_{termes_a_rechercher}.csv")

    return df


def create_benchmark_from_topics(topics):
    client = twitter_client_authentification()

    benchmark_columns = INTERRESTING_COLUMNS.copy().append('label')
    benchmark = pd.DataFrame(columns=benchmark_columns)

    for topic in topics:
        # On choisit un nombre aléatoire entre 10 et 100 pour ne pas avoir uniquement des classes homogènes
        rand_number = randint(10, 100)
        print(f"topic : {topic} - rand_number : {rand_number}")

        # On crée un dataframe de tweets contenant le topic
        df = search_tweets(client, topic, max_results=rand_number, tweet_fields=INTERRESTING_COLUMNS, save_result=False)

        # On ajoute une colonne 'label' pour specifier à quel topic appartiennent ces tweets
        df['label'] = topic  # le topic sera répété pour toutes les lignes de df

        # On concatene les tweets avec le benchmark
        benchmark = pd.concat([benchmark, df])

    return benchmark


def create_benchmark_from_ids(base_dir_path):
    # Liste des fichiers états (AK.csv par exemple)
    list_state_csv = os.listdir(base_dir_path)

    # Dataframe qui va contenir les tweets recuperés
    df_results = pd.DataFrame()

    # Pour chaque fichier du dossier covid (AK.csv par exemple)
    for state_csv in list_state_csv:
        # On lit le csv et on recupère les identifints des tweets
        df_state_csv = pd.read_csv(base_dir_path + state_csv)
        list_state_tweet_id = df_state_csv['Tweet_ID'].values

        rand_number = randint(10, 100)

        list_id = [str(x) for x in list_state_tweet_id[:rand_number]]

        # On appelle l'api twitter pour recupérer les tweets correspondant aux ids
        client = twitter_client_authentification()
        df_result_tmp = get_tweets_by_id(client, list_id)

        # On crée une nouvelle colonne "state" contenant le nom du fichier (AK p.e) pour garder en memoire l'état
        df_result_tmp.loc[:, 'state'] = state_csv.split(".")[0]

        df_results = pd.concat([df_results, df_result_tmp])

    # On enregistre le resultats au format csv
    df_results.to_csv("../../data/resultats2.csv")

    return df_results


def create_benchmark_from_id_file(file_path):
    # Lire le fichier des ids
    ids = list(pd.read_csv(file_path)['Tweet_ID'].values)
    random.shuffle(ids)
    ids = ids[610000:]

    # Authentification api
    client = twitter_client_authentification()

    decoupage = np.arange(0, len(ids), 99)

    df_results = pd.DataFrame()
    n = 10000

    for i in range(len(decoupage) - 1):
        print("Tweets de " + str(decoupage[i]) + " à " + str(decoupage[i + 1]))
        list_ids = [str(x) for x in ids[decoupage[i]:decoupage[i + 1]]]
        df_result_tmp = get_tweets_by_id_with_geo(client, list_ids)

        df_results = pd.concat([df_results, df_result_tmp])

        if decoupage[i] >= n:
            df_results.to_csv("../../data/resultats/results_" + str(n+610000) + ".csv")
            n += 10000

    return df_results


if __name__ == "__main__":
    # path = "../../data/Tweets_United_States.csv"
    # df = create_benchmark_from_id_file(path)
    # df.to_csv("../../data/results.csv")

    df_results = pd.DataFrame()
    results_dir = os.listdir("../../data/resultats/")
    for res in results_dir:
        if res.split(".")[1] == "csv":
            df_res = pd.read_csv("../../data/resultats/" + res)
            df_res = df_res.drop(columns=['Unnamed: 0'])
            df_results = pd.concat([df_results, df_res])

    df_results.drop_duplicates(subset=['id'], keep='last')
    df_results = df_results.sample(frac=1).reset_index(drop=True)
    df_results.to_csv("../../data/results.csv")

