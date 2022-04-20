# Import #
import get_data
from textblob import TextBlob


#sentiment analysis of a given tweet
def sentiment_analysis(tweet):
    '''
    Parameters
    ----------
    tweet : DATAFRAME
        dataframe of tweets.

    Returns
    -------
    DATAFRAME
        dataframe of tweets with a sentiment analysis of each tweet.

    '''
    #function to get the subjectivity
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity
      
    #function to get the polarity
    def getPolarity(text):
        return TextBlob(text).sentiment.polarity
      
    #Create two new columns ‘Subjectivity’ & ‘Polarity’
    tweet['TextBlob_Subjectivity'] = tweet['tweet'].apply(getSubjectivity)
    tweet['TextBlob_Polarity'] = tweet['tweet'].apply(getPolarity)
    
    def getAnalysis(score):
        if score < 0 :
            return 'Negative'
        
        elif score == 0 :
            return 'Neutral'
        
        else :
            return 'Positive'
    
    tweet['TextBlob_Analysis'] = tweet['TextBlob_Polarity'].apply(getAnalysis)
      
    return tweet



#requete = "Covid-19 OR Covid OR Corona OR Pandémie OR épidémie OR Coronavirus OR virus"
#number=1000

#df_tweets = get_data.get_tweets(requete, number)

#new_df_tweets = sentiment_analysis(df_tweets)

#new_df_tweets.to_csv('dataframe.csv')







