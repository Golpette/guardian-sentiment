#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################
# VADER sentiment analysis across news themes
######################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from vaderSentiment.vaderSentiment  import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import math

DATAFILE = "scraped_data.csv"
OUTPUT = "guardian_senitments.png"
STAT = "mean_sentence"


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





def main():

    # Read in csv
    df = pd.read_csv(DATAFILE)

    # Add column with mean sentence compound sentiment
    df[STAT] = df['article'].map( lambda x: mean_sentiment_from_sentences(x) )

    groups = df.groupby("theme")

    # Make violin plots for each theme
    ncols = 3
    f, axes = plt.subplots(nrows=2, ncols=ncols)
    for i,(nm,grp) in enumerate(groups):
        sns.violinplot(  y=STAT, data=grp, ax=axes[i//ncols][i%ncols], inner=None, alpha=0.5)
        sns.swarmplot(  y=STAT, data=grp , ax=axes[i//ncols][i%ncols], alpha=0.9, color="black")
        axes[i//3][i%3].set_title(nm)
        axes[i//3][i%3].set_ylabel("Sentiment")
        axes[i//3][i%3].set_ylim(-1,1)
    f.tight_layout()

    plt.savefig(OUTPUT)

    plt.show()





if __name__ == "__main__":
    main()
