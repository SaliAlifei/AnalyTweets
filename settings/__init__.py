import os
from dotenv import load_dotenv

# Chemin absolu vers le fichier env_var.env de parm
PATH_TO_ENV_FILE = "C:/Users/Salimata/Documents/Projets/AnalyTweets/parm/env_var.env"


def load_env():
    load_dotenv(PATH_TO_ENV_FILE)


if __name__ == "__main__":
    load_env()
    print(os.environ.get("TWITTER_API_KEY"))
