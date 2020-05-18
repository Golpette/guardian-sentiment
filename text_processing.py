#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Regexp and scraping
from bs4 import BeautifulSoup
import requests
import re 


def get_article_content( link ):
    """ Get single String of article body from URL """
    page = requests.get(link).text
    lines = page.split("\n")

    article = ""
    article_started = False
    article_finished = False

    for line in lines:
        if 'itemprop="articleBody' in line:
            article_started = True
        if 'class="after-article' in line:
            article_finished = True
        
        if (article_started and not article_finished):
            article = article + " " + line

    #article = tidy_article( article )
    return article


def tidy_article_allow_punct( text ):
    """ Tidy up body of article but preserve punctuation
    for the sentiment analysis """ 
    #Get rid of new lines. Need this for the <figure> removal
    text = text.replace('\n', ' ').replace('\r', '')
    #<figure> tag has contents. Remove all this.
    text = re.sub( '<figure(.*?)/figure>', '', text)
    #<span> contains "facebook twitter google plus bst"
    text = re.sub( '<span(.*?)/span>', '', text)
    #<sup> is a little supplementary notice
    text = re.sub( '<sup(.*?)/sup>', '', text)
    #"Read more" text
    text = re.sub( '<div class="rich-link__read-more(.*?)/div>', '', text)
    text = re.sub( 'Read more here:', '', text)
    #Remove other html tags but keep content
    text = re.sub( '<[^>]+>', ' ', text) 
    #Remove numbers
    text = ' '.join(s for s in text.split() if not any(c.isdigit() for c in s))
    # Remove contractions
    text = re.sub('\'s', '', text)
    text = re.sub('’s', '', text)  
    #Remove extra spaces
    text = re.sub('\s+', ' ' , text)        
    return text.strip()





def tidy_article( text ):
    """ Tidy up body of article and remove punctuation """ 
    #Get rid of new lines. Need this for the <figure> removal
    text = text.replace('\n', ' ').replace('\r', '')
    #<figure> tag has contents. Remove all this.
    text = re.sub( '<figure(.*?)/figure>', '', text)
    #<span> contains "facebook twitter google plus bst"
    text = re.sub( '<span(.*?)/span>', '', text)
    #<sup> is a little supplementary notice
    text = re.sub( '<sup(.*?)/sup>', '', text)
    #"Read more" text
    text = re.sub( '<div class="rich-link__read-more(.*?)/div>', '', text)
    text = re.sub( 'Read more here:', '', text)
    #Remove other html tags but keep content
    text = re.sub( '<[^>]+>', ' ', text) 
    #Remove numbers
    text = ' '.join(s for s in text.split() if not any(c.isdigit() for c in s))
    # Remove contractions
    text = re.sub('\'s', '', text)
    text = re.sub('’s', '', text)
    #text = re.sub('n\'t', ' not', text)  
    #text = re.sub('s\'', 's', text)
    #text = re.sub('I\'m', 'I am', text)
    ##(  she'd ->  she would, OR she had;
    # Remove punctuation but leave hyphenated words 
    text = re.sub(' - ', ' ', text)
    text = re.sub('–', ' ' , text )
    text = re.sub('-', ' ', text)
    text = re.sub(r'[?|$|.|!|)|\]|\[|(|"|“|”|’|,|:|\']', r'', text)  
    #Remove extra spaces
    text = re.sub('\s+', ' ' , text)        
    return text.strip()
