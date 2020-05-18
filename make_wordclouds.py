#####################################
# Make wordclouds of each news theme
#####################################

import sys; sys.dont_write_bytecode=True

from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import text_processing as tp

MASK_IMG = "data/g_icon.png"
DATAFILE = "data/scraped_data.csv"

OUT_ROOT = "wordcloud_"

###################

def transform_format(val):
    """Transform B&W (True,False) to (255,1)"""
    if val==True:
        return 255
    else:
        return 1


def mask_from_bw( BW_img ):
    """Convert B&W image (True, False) to (255, 1) for use as mask"""
    img = np.array(Image.open( BW_img ))
    # Transform your mask into a new one that will work with the function:
    transformed_img = np.ndarray( (img.shape[0], img.shape[1]), np.int32  ) 
    for i in range( len(img) ):
        transformed_img[i] = list( map(transform_format, img[i])  )
    return transformed_img



def wordcloud_with_mask( word_occurrence, mask_img, output_file ):
    """Make wordcloud using dict of word occurrences and mask"""

    mask = mask_from_bw( mask_img )

    #wordcloud = WordCloud(width=1600, height=800, max_font_size=200).generate( article )
    #wordcloud = WordCloud(width=1600, height=800, max_font_size=200, background_color="white").generate_from_frequencies( word_occurrences_no_stopwords )
    #wordcloud = WordCloud(background_color=None, width=1600, height=800, mask=transformed_img,
    #            stopwords=stopwords, contour_width=2, contour_color='white', mode='RGB',
    #            colormap='Dark2').generate_from_frequencies( word_occurrences_no_stopwords )
    wordcloud = WordCloud(background_color='black', mask=mask,
                contour_width=2, contour_color='white',
                colormap='Dark2').generate_from_frequencies( word_occurrence )
    #max_font_size=200,
    wordcloud.to_file( output_file )
    plt.figure(figsize=(12,10)) #Make this match size of the mask
    ##plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    #plt.show()



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



def read_stopwords(filename):
    """Read file with 1 stopword/line"""
    stopwords=[]
    file = open(filename, 'r')  
    for line in file:
        stopwords.append( line.strip() )
    return stopwords






def main( datafile=None ):

    if datafile is None:
        print("Using example data file")
        datafile = DATAFILE

    stopwords = read_stopwords("data/stopwords.txt")

    df = pd.read_csv(datafile)

    groups = df.groupby("theme")

    
    
    for name,grp in groups:
    
        print("name = {}".format(name))
        
        fileout = OUT_ROOT + name + ".png"

        # Join all articles in theme
        all_articles = grp["article"].str.cat(sep=" ")
        #all_articles = ""
        #for row,data in grp.iterrows():
        #    all_articles = all_articles+" "+data["article"]

        # Lose punctuation for wordlcouds
        all_articles = tp.tidy_article( all_articles ).lower()

        # Dict with words and counts
        word_occurrences_no_stopwords = {}
        word_occurrences_no_stopwords = accumulate_words( all_articles, 
                                word_occurrences_no_stopwords, stopwords )

        #Make wordcloud and save as png
        wordcloud_with_mask( word_occurrences_no_stopwords, MASK_IMG, fileout )       
        





if __name__ == "__main__":
    main()






