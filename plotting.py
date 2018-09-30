import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Bokeh interaxctive plots
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.models import HoverTool
from bokeh.embed import file_html
from bokeh.resources import CDN



def bokeh_wordcount( dataframe, max_words, fileout):
    """Make bokeh html plot of word occurrences"""
    p = figure(x_axis_label='Rank', y_axis_label='Count', y_axis_type='log')
    #Only use 100 higest ranking words
    p.circle('rank', 'count', size=10, alpha=0.4, 
            color='forestgreen', source=dataframe[:max_words])
    hover = HoverTool(tooltips=[('token','@index')])
    p.add_tools(hover)

    html = file_html(p, CDN, "Word occurrences")
    f = open( fileout, 'w')
    f.write( html )
    f.close()



def sentiment_hist( df, col_name, bins, outfile ):
    #Make histogram of sentiments and save file
    plt.figure()
    plt.xlim([-1.0, 1.0])
    plt.rc('axes', labelsize=13)
    plt.rc('xtick', labelsize=11)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=11)
    plt.rc('figure', titlesize=15)
    ax = df[col_name].plot.hist(bins=bins)
    ax.set(xlabel=col_name, title="Distribution of article sentiments")
    plt.savefig( outfile )




#df = pd.read_csv( "article_sentiments.csv" )
#sentiment_hist( df, 'mean_sentence_compound', 10, "out.png")
