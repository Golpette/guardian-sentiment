# Regexp and scraping
from bs4 import BeautifulSoup
import urllib2
import urllib    
import re 



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
    links_found=[]
    print page
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



def spider( start_page, theme, max_urls ):
    """Spider from start_page and get related urls

    Theme is the subject, i.e. /sport/, /books/    
    """
    theme = "/"+theme.lower()+"/"

    to_visit = []
    visited = []
    visited.append( start_page )
    to_visit = get_related_links( start_page, theme, to_visit, visited )

    while len(visited) < max_urls+1:

        # collect as many urls as possible up to twice the desired amount
        #  - some collected won't be articles
        if len(to_visit)==0 or len(visited)==max_urls:
            #remove non-story root page
            visited.pop(0)
            return visited

        url = to_visit.pop(0)
        visited.append( url )
        to_visit += get_related_links( url, theme, to_visit, visited )



#urls = spider("https://theguardian.com/books", "books/2018", 10);
#for url in urls:
#    print url


        

