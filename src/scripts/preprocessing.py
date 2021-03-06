import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from settings import UNINTERRESTING_WORDS
nltk.download("omw-1.4", quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)


lemmatizer = WordNetLemmatizer()

stop_words = stopwords.words("english")

emojis = re.compile("["
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


def clean_texts(texts, stop_words=stop_words, emojis=emojis, delete_sup_words=False):
    cleaned_texts = []

    for text in texts:
        text = str(text)

        # Suppression des url
        text = re.sub(r'https?://\S+|www\.\S', '', text)

        # Suppression des ponctuations
        punctuations = r'''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for character in text.lower():
            if character in punctuations:
                text = text.replace(character, "")

        # Suppression des stopwords
        text = ' '.join([word for word in text.split() if word not in stop_words])

        if delete_sup_words:
            # Suppression des mots supplementaires
            text = ' '.join([word for word in str(text).split() if word not in UNINTERRESTING_WORDS])

        # Suppression des chiffres
        text = re.sub(r'[0-9]+', '', text)

        # Lemmatisation
        text = ' '.join([lemmatizer.lemmatize(words) for words in text.split()])

        # Suppression des emojis
        text = re.sub(emojis, '', text)

        # Suppression des textes contenant moins de 5 mots
        # if len(text.split(" ")) < 5:
        #    continue

        cleaned_texts.append(text)

    return cleaned_texts


def bag_of_words(texts, as_array=False):
    cv = CountVectorizer()
    bow = csr_matrix(cv.fit_transform(texts))
    feature_names = cv.get_feature_names()

    if as_array:
        return [bow.toarray(), feature_names]

    return [bow, feature_names]


def preprocess(texts):
    cleaned_texts = clean_texts(texts, stop_words, emojis)
    bow, feature_names = bag_of_words(cleaned_texts, as_array=False)
    return [bow, feature_names]


if __name__ == "__main__":
    path_to_test_file = "../../data/results.csv"

    df = pd.read_csv(path_to_test_file)
    texts = df['text'].values

    print(texts[:2])
    print(f"Taille textes d??part : {len(texts)}\n")

    cleaned_texts = clean_texts(texts, stop_words, emojis)
    print(cleaned_texts[:2])
    print(f"Taille textes nettoy??s : {len(cleaned_texts)}\n")

    df.loc[:, "cleaned_texts"] = cleaned_texts
    df.to_csv("../../data/original_df.csv")

    """
    bow, feature_names = bag_of_words(cleaned_texts, as_array=False)
    print(f"Shape matrice bag of words : {bow.shape}")
    print(f"Taille vocabulaire : {len(feature_names)}")
    print(feature_names)
    """

