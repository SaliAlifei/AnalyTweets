import pandas as pd
from sklearn.decomposition import NMF, LatentDirichletAllocation
from src.scripts.preprocessing import preprocess


def nmf(X, k, init='random', random_state=0):
    model = NMF(n_components=k,
                init=init,
                random_state=random_state)
    w = model.fit_transform(X)
    h = model.components_
    return [model, w, h]


def lda(X, k, init='random', random_state=0):
    model = LatentDirichletAllocation(n_components=k,
                                      random_state=random_state)
    return [model, model.fit_transform(X)]


# Source : https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
def get_n_top_words(n, model, feature_names):
    top_words = []
    top_weights = []
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[: -(n+1):-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        top_words.append(top_features)
        top_weights.append(weights)
    return [top_words, top_weights]


if __name__ == "__main__":
    path_to_test_file = "C:/Users/salim/Documents/Cours/PPD/AnalyTweets/data/benchmark.csv"
    texts = pd.read_csv(path_to_test_file)['text'].values

    k = 10
    X, feature_names = preprocess(texts)

    lda_model, resultat_lda = lda(X, k)

    nmf_model, w, h = nmf(X, k)

    print("\n\n ----------------- \n\n")

    print(get_n_top_words(5, nmf_model, feature_names))
    print(get_n_top_words(5, lda_model, feature_names))
