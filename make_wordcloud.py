from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


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



def with_mask( word_occurrence, mask_img, output_file ):
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
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    #plt.show()
