# Run all analyses on scraped data:
#  1. Make word clouds of each theme
#  2. Sentiment analysis of each theme
#  3. Word frequency plots

import make_wordclouds
import sentiment_analyser
import word_frequency

#DATAFILE = "data/scraped_data.csv"
DATAFILE = "scraped_data.csv"

def main():
    print("Making word clouds, will take a minute...")
    make_wordclouds.main(DATAFILE)
    print("Doing sentiment analysis...")
    sentiment_analyser.main(DATAFILE)
    print("Making word frquency plots...")
    word_frequency.main(DATAFILE)
    

if __name__=="__main__":
    main()
