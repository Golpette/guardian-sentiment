# Sentiment analysis
from vaderSentiment.vaderSentiment  import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import numpy as np
import math


def sentiment_score( text ):
    """ VADER polarity scores """
    analyser = SentimentIntensityAnalyzer()
    sentiment = analyser.polarity_scores( text )
    #sentiment is dict with {'neg', 'neu', 'pos', 'compound'}
    return sentiment


def mean_sentiment_from_sentences( text ):
    """Use nltk to tokenize to sentences and return
     mean compound score"""
    #Tokenizer only accepts ascii 
    sentences = sent_tokenize( text.decode("ascii", errors="ignore").encode() )
    #sentence_scores = []
    list_compound_scores = []
    for sentence in sentences:
        sentiment = sentiment_score( sentence )
        #sentence_scores.append( sentiment )
        list_compound_scores.append( sentiment['compound'] )
    #TODO: Here we do not consider neutral sentences in average!
    #return np.mean( list_compound_scores )
    return np.mean( [v for v in list_compound_scores if v!=0] )



def compound_alter_alpha( compound, alpha ):
    """ Recalculate compound sentiment with altered alpha parameter
 
        In the VADER normalisation alpha is hardcoded as 15.      
    """ 
    # Normalisation: compound = x / sqrt( x**2 + alpha ), where x is 
    # sum of individual lexicon sentiments scores 
    sign = compound/abs(compound)
    x = sign * math.sqrt( (15.0*compound**2)/(1-compound**2) )
    new_compound = x / ( math.sqrt(x**2+alpha) )
    return new_compound

    
