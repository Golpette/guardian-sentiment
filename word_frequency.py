import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Bokeh interaxctive plots
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.models import HoverTool
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.layouts import gridplot
# select a palette
from bokeh.palettes import Category10_7 as palette
# itertools handles the cycling
import itertools 
# mine
import text_processing as tp



DATAFILE = "scraped_data.csv"
OUT_ROOT = "word_freq_"
OUTPUT = "word_frequencies.html"
MAX_WORDS = 50






def bokeh_wordcount( ranked_dataframe, max_words, fileout):
    """Make bokeh html plot of word occurrences"""
    p = figure(x_axis_label='Rank', y_axis_label='Count', y_axis_type='log')
    #Only use 100 higest ranking words
    p.circle('rank', 'count', size=10, alpha=0.4, 
            color='forestgreen', source=ranked_dataframe[:max_words])
    hover = HoverTool(tooltips=[('token','@index')])
    p.add_tools(hover)

    html = file_html(p, CDN, "Word occurrences")
    f = open( fileout, 'w')
    f.write( html )
    f.close()



def accumulate_words( text, worddic, stopwords=None ):
    """ Count and store occurrences of each word in a dictionary"""   
    words = text.split()
    if stopwords is None:
        for word in words:
            # Remove numbers, hashtags and emails
            #if not any(char.isdigit() for char in word) and '#' not in word and '@' not in word:    ## DO THIS IN TIIDY METHOD
            if word in worddic:
                worddic[ word ] += 1
            else:
                worddic[ word ] = 1
    else:
        for word in words:
            if word in worddic and word not in stopwords:
                worddic[ word ] += 1
            elif word not in stopwords:
                worddic[ word ] = 1

    return worddic



def make_ranked_df( dic ):
    """Make a pandas df from our dictionary of word_occurrences. Add word rank"""
    new_dic={}
    rank=0
    # Sort by value and add rank to new dictionary
    for key,value in sorted(dic.iteritems(), key=lambda (k,v): v, reverse=True):
        rank += 1
        new_dic[key]=[rank,value]
    #Make pandas df from this
    df = pd.DataFrame.from_dict( new_dic, orient='index', columns=['rank','count'] )
    return df



def read_stopwords(filename):
    """Read file with 1 stopword/line"""
    stopwords=[]
    file = open(filename, 'r')  
    for line in file:
        stopwords.append( line.strip() )
    return stopwords







def main():

    stopwords = read_stopwords("stopwords.txt")

    df = pd.read_csv(DATAFILE)

    groups = df.groupby("theme")

    #List of figs for gridplot
    figs_grid = []

    colors = itertools.cycle(palette)    

    
    for (name,grp),color in zip(groups,colors):
        
        fileout = OUT_ROOT + name + ".html"

        all_articles = ""
        # Join all articles
        #articles = grp["article"].agg(lambda x: ' '.join(x))
        for row,data in grp.iterrows():
            all_articles = all_articles+" "+data["article"]

        # Lose punctuation for wordlcouds
        all_articles = tp.tidy_article( all_articles ).lower()

        # Dict with words and counts
        word_occurrences_no_stopwords = {}
        word_occurrences_no_stopwords = accumulate_words( all_articles, 
                                word_occurrences_no_stopwords, stopwords )

        #Make dataframe from dic and sort it by rank
        ranked_df = make_ranked_df( word_occurrences_no_stopwords )
        ranked_df = ranked_df.sort_values('rank', axis=0)
        
        #Make interactive Bokeh plot and save as html
        #bokeh_wordcount( ranked_df, MAX_WORDS, fileout )


        # Make list of plots for gridplot layout        
        p = figure(x_axis_label='Rank', y_axis_label='Count', 
                y_axis_type='log', title=name)
        p.circle('rank', 'count', size=10, alpha=0.6, 
                color=color, source=ranked_df[:MAX_WORDS])    #'forestgreen'
        hover = HoverTool(tooltips=[('token','@index')])
        p.add_tools(hover)
        figs_grid.append(p)




    # put all the plots in a grid layout
    gridfig = gridplot( [ figs_grid[0:3], figs_grid[3:6] ] )

    html = file_html(gridfig, CDN, "Word occurrences")
    f = open( OUTPUT, 'w')
    f.write( html )
    f.close()

    # show the results
    #show(gridfig)




 
        


if __name__ == "__main__":
    main()

















#df = pd.read_csv( "article_sentiments.csv" )
#sentiment_hist( df, 'mean_sentence_compound', 10, "out.png")
