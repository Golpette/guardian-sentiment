#!/usr/bin/env python
# -*- coding: utf-8 -*-
##################################
# Bokeh html plot showing word
# frequencies across topics
##################################
import sys; sys.dont_write_bytecode=True

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



DATAFILE = "data/scraped_data.csv"
OUT_ROOT = "word_freq_"
OUTPUT = "word_frequencies.html"
MAX_WORDS = 50






def bokeh_wordcount( ranked_dataframe, fileout, max_words=None):
    """Make bokeh html plot of word occurrences"""

    if max_words==None:
        max_words = len(ranked_dataframe.index)-1

    p = figure(x_axis_label="Rank", y_axis_label="Count", 
            y_axis_type="log", x_axis_type="log")
    #Only higest ranking words
    p.circle("rank", "count", size=10, alpha=0.4, 
            color="forestgreen", source=ranked_dataframe[:max_words])
    hover = HoverTool(tooltips=[("token","@index")])
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
    #for key,value in sorted(dic.iteritems(), key=lambda (k,v): v, reverse=True):
    for key in sorted(dic, key=dic.get, reverse=True):
        value = dic[key]
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







def main( datafile=None ):

    if datafile is None:
        print("word_freuency.py using example data set")
        datafile = DATAFILE

    df = pd.read_csv(datafile)
    groups = df.groupby("theme")

    stopwords = read_stopwords("data/stopwords.txt")

    #List of figs for gridplot
    figs_grid = []

    colors = itertools.cycle(palette)    
    all_words = {}

    
    for (name,grp),color in zip(groups,colors):
        
        # Join all articles in theme
        all_articles = grp["article"].str.cat(sep=" ")

        # Drop punctuation for word freqs
        all_articles = tp.tidy_article( all_articles ).lower()

        # All words for Zipfs law, including stopwords
        all_words = accumulate_words( all_articles, all_words )

        # Dict with words and counts
        word_occurrences_no_stopwords = {}
        word_occurrences_no_stopwords = accumulate_words( all_articles, 
                                word_occurrences_no_stopwords, stopwords )

        ranked_df = make_ranked_df( word_occurrences_no_stopwords )
        ranked_df = ranked_df.sort_values("rank", axis=0)

        # Make list of plots for gridplot layout        
        #p = figure(x_axis_label="Rank", y_axis_label="Count", 
        #        x_axis_type="log", y_axis_type="log", title=name)
        p = figure(x_axis_label="Rank", y_axis_label="Count", 
                title=name)
        p.circle("rank", "count", size=10, alpha=0.6, 
                color=color, source=ranked_df[:MAX_WORDS])    #'forestgreen'
        hover = HoverTool(tooltips=[("token","@index")])
        p.add_tools(hover)
        figs_grid.append(p)


        # -- Each topic
        #fileout = OUT_ROOT + name + ".html"
        #Make dataframe from dic and sort it by rank
        #ranked_df = make_ranked_df( word_occurrences_no_stopwords )
        #ranked_df = ranked_df.sort_values("rank", axis=0)
        #
        #Make interactive Bokeh plot and save as html
        #bokeh_wordcount( ranked_df, fileout, MAX_WORDS )




    # put all the plots in a grid layout
    gridfig = gridplot( [ figs_grid[0:3], figs_grid[3:6] ] )
    html = file_html(gridfig, CDN, "Word occurrences")
    f = open( OUTPUT, 'w')
    f.write( html )
    f.close()

    # show the results
    #show(gridfig)


    #Make Bokeh plot for Zipfs law of all articles
    rank_df = make_ranked_df( all_words )
    rank_df = rank_df.sort_values("rank", axis=0)
    bokeh_wordcount( rank_df, "zipf.html" )




if __name__ == "__main__":
    main()



