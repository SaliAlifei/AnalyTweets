import os
from dotenv import load_dotenv

# Constantes
NB_TOPICS = 10
UNINTERRESTING_WORDS = ["covid", "covid19", "coronavirus", "corona", "virus", "pandemic", "covid2019", "covid-19", "amp", "#amp"
                        "#covid", "#covid19", "#coronavirus", "#corona", "#virus", "#pandemic", "#covid2019", "#covid-19"]


# Chemin absolu vers le fichier env_var.env de parm
PATH_TO_ENV_FILE = "C:/Users/Salimata/Documents/Projets/AnalyTweets/parm/env_var.env"


def load_env():
    load_dotenv(PATH_TO_ENV_FILE)


if __name__ == "__main__":
    load_env()
    print(os.environ.get("TWITTER_API_KEY"))
