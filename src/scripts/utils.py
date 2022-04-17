import pandas as pd
from wordcloud import WordCloud
from src.scripts.tweets import get_tweet_by_id, twitter_client_authentification
from src.scripts.preprocessing import preprocess
from src.scripts.models import nmf, get_n_top_words


def wordcloud(df, state="all", max_words=400, save=False):
    if state == "all":
        texts = df["cleaned_texts"].values
    else:
        texts = df[df["state"] == state]["cleaned_texts"].values

    if len(texts) == 0:
        texts = ["NoEntry"]

    text = " ".join(str(review) for review in texts)
    wordcloud = WordCloud(width=550, height=300, background_color='#052140', max_words=max_words).generate(text)

    if save:
        # saving wordcloud as image
        wordcloud.to_file("../../data/wordcloud-state.png")

    return wordcloud.to_image()


def get_topics_by_url(url):
    id = url.split("/")[-1]

    client = twitter_client_authentification()
    tweet = get_tweet_by_id(client, id, with_geo=True)

    if tweet:
        # On charge le dataset
        path_to_dataset = "../../data/resultats/shuflled_0_a_300.csv"
        df = pd.read_csv(path_to_dataset)
        df = df.drop(columns=['Unnamed: 0'])

        # On ajoute le nouveau tweet à la fin du dataset
        tweet_index = df.shape[0]
        df.loc[tweet_index] = tweet

        # On lance le modèle
        topics = 10
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


def add_states_lat_long(dataframe):
    df = pd.read_csv("../../data/statelatlong.csv")
    df_merged = pd.merge(dataframe, df, on=["state"])
    df_merged = df_merged.drop(columns=["Unnamed: 0", "Unnamed: 0.1", "Unnamed: 0.1.1", "City"])
    return df_merged


if __name__ == "__main__":
    """
    df = pd.read_csv("../../data/resultats.csv")
    df_merged = add_states_lat_long(df)
    df_merged.to_csv("../../data/covid/resultats_latlong.csv")
    """

    get_topics_by_url("hfei")
