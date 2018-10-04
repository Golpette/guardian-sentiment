#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################
# Scraping set number of urls from specifiec news 
# themes. Save url, text, date, theme to a csv file
######################################################

import sys
sys.dont_write_bytecode = True

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
# Regexp and scraping
from bs4 import BeautifulSoup
import urllib2
import urllib    
import re 
# My modules
import text_processing as tp


##############################################
URL = "https://www.theguardian.com/"
#THEMES = ['world', 'sport']
THEMES = ["world", "politics", "books", 
        "sport", "film", "environment"]
NO_URLS = 100
##############################################


def scrape_links( page ):
    """Retrieve all Guardian article links from current page"""
    #Ignore /info/ and /help/ links
    to_visit = []
    resp = urllib2.urlopen( page )
    soup = BeautifulSoup(resp, 'lxml')
    for link in soup.find_all('a', href=True):
        if( '//www.theguardian' in link['href'].lower() ):
            if( '/help/' not in link['href'].lower() and 
              '/info/' not in link['href'].lower() ):
                if link['href'] not in to_visit:
                    to_visit.append( link['href'] )
    return to_visit



def get_related_links( page, theme, to_visit, visited ):
    """ Retrieve "More on this story" links from current page
        and update list of visited and to_visit pages
    """
    theme = "/"+theme.lower()+"/"
    links_found=[]
    #print page
    try:
        resp = urllib2.urlopen( page )
        soup = BeautifulSoup(resp, 'lxml')
        for link in soup.find_all('a', href=True):
            if theme in link['href'].lower() and '//www.theguardian' in link['href'].lower():
                if( '/help/' not in link['href'].lower() and '/info/' not in link['href'].lower() ):
                    if( link['href'] not in to_visit and link['href'] not in visited
                            and link['href'] not in links_found):
                        links_found.append( link['href'] )
    except urllib2.HTTPError:
        # Dead link found 
        print "dead link"
    return links_found



def spider_scrape_theme( start_page, theme, max_urls ):
    """Spider from start_page and scrape stories from related urls
    Theme is the subject, i.e. /sport/, /books/    
    """
    articles_found = 0

    data_list = []

    to_visit = []
    visited = []
    visited.append( start_page )

    to_visit = get_related_links( start_page, theme, to_visit, visited )

    while articles_found < max_urls+1:

        # collect as many urls as possible up to twice the desired amount
        #  - some collected won't be articles
        if len(to_visit)==0 or articles_found==max_urls:
            #remove non-story root page
            visited.pop(0)
            #return dataframe of theme
            df = pd.DataFrame( data_list )
            #reorder cols
            ##df = df[["theme", "url", "article", "length"]]
            return df            

        url = to_visit.pop(0)
        visited.append( url )
        to_visit += get_related_links( url, theme, to_visit, visited )

        article_raw = tp.get_article_content( url )
        ###date = get_date_published( url )
        # Keep punctuation for sentiment analysis
        article_tidy = tp.tidy_article_allow_punct( article_raw )
        if len(article_tidy.split())>20:
            data_list.append( {"theme":theme.lower(), "url":url, "article":article_tidy, "length":len(article_tidy.split())} )
            articles_found += 1
            if (articles_found%5==0):
                print theme, ": articles =", articles_found


def get_date_published( link ):
    """ Get article's publish date """
    ol = urllib.urlopen( link )
    date = ""
    next_line = False
    for line in ol:
        if next_line:
            next_line = False
            date = tidy_article(line)
        if 'datePublished' in line:
            next_line = True   
    return date

###################################



def main():

    frames = []
    for theme in THEMES:

        start_page = URL+theme
        visited = []
        visited.append( start_page )

        # Try for twice as many urls as wanted incase some are not articles
        dataframe = spider_scrape_theme( start_page, theme, NO_URLS )
        #print dataframe

        frames.append( dataframe )    

    #Concat to single dataframe to csv
    df = pd.concat( frames )
    df.to_csv( "scraped_data.csv" )




if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()




