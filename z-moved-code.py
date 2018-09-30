#TODO:
# Could ignore "live update" stuff, as not technically articles
# Recover the first letter of article
# Alter stopwords to improve wordclouds


#stopwords = read_stopwords('stopwords.txt')


WORDCLOUD_FILENAME = "wordcloud.png"
MASK_IMG = "g_icon.png"

BOKEH_FILENAME = "word-occurrences.html"
MAX_WORDS_TO_DISPLAY = 50

ARTICLE_SENTIMENTS = "article_sentiments.csv"
SENTIMENT_HISTO = 'sentiments.png'




def accumulate_words( text, wordlist, stopwords=None ):
    """ Count and store occurrences of each word in a dictionary"""   
    words = text.split()
    if stopwords is None:
        for word in words:
            # Remove numbers, hashtags and emails
            #if not any(char.isdigit() for char in word) and '#' not in word and '@' not in word:    ## DO THIS IN TIIDY METHOD
            if word in wordlist:
                wordlist[ word ] += 1
            else:
                wordlist[ word ] = 1
    else:
        for word in words:
            if word in wordlist and word not in stopwords:
                wordlist[ word ] += 1
            elif word not in stopwords:
                wordlist[ word ] = 1

    return wordlist


def read_stopwords(filename):
    """Read file with 1 stopword/line"""
    stopwords=[]
    file = open(filename, 'r')  
    for line in file:
        stopwords.append( line.strip() )
    return stopwords


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





    '''
    article_count=0
    word_occurrences = {}
    word_occurrences_no_stopwords = {}
    sentiments = {}

    mean_sentence_compound=[]
    

    article=""
    while len(to_visit)>0 and len(visited)<NO_URLS:
    #while article_count<5 and len(to_visit)>0:

        url = to_visit.pop(0)
        visited.append( url )
        #date = get_date_published( url )
        
        article = gt.get_article_content( url )

        # Keep punctuation for sentiment analysis
        article_with_punct = gt.tidy_article_allow_punct( article )
        article = gt.tidy_article( article ).lower()

        if len(article) > 20:
            article_count += 1
            #Save article
            #filename = "article_"+str( len(visited) )+".txt"
            #file = open( filename, 'w' )
            #file.write( url + "\n" )
            ##file.write( date + "\n")
            #file.write( article )
            #file.close()

            # Article length can affect the compound sentiment score
            no_words = len( article_with_punct.split() )

            word_occurrences = accumulate_words( article, word_occurrences )
            word_occurrences_no_stopwords = accumulate_words( article, 
                                    word_occurrences_no_stopwords, stopwords )

            # Whole article sentiment plus sentence mean
            article_sentiment = vs.sentiment_score( article_with_punct )
            mean_sentence_compound = vs.mean_sentiment_from_sentences( article_with_punct ) 

            #dict of article properties to be converted to dataframe 
            sentiments[str(article_count)] = [ url, no_words, article_sentiment['neg'],
                           article_sentiment['neu'], article_sentiment['pos'], 
                           article_sentiment['compound'], mean_sentence_compound ]
        

            # Calculate whole-article compound scores for various alpha parameters
            alphas = [30,50,150,300,400]
            for alpha in alphas:
                new_compound = vs.compound_alter_alpha( article_sentiment['compound'], alpha )
                sentiments[ str(article_count) ] += [new_compound]

    

    #print word_occurrences
    #print word_occurrences_no_stopwords
    #print len(word_occurrences)
    #print len(word_occurrences_no_stopwords)
    print "Article count = ", article_count

    #Make dataframe from dic and sort it by rank
    df = make_ranked_df( word_occurrences_no_stopwords )
    df = df.sort_values('rank', axis=0)
    #Make interactive Bokeh plot and save as html
    plotting.bokeh_wordcount( df, MAX_WORDS_TO_DISPLAY, BOKEH_FILENAME )

    #Make wordcloud and save as png
    make_wordcloud.with_mask( word_occurrences_no_stopwords, MASK_IMG, WORDCLOUD_FILENAME )

    #Make pandas df for WHOLE-ARTICLEE sentiments; save to file
    cols=['url','article_length','neg','neu','pos','compound', 'mean_sentence_compound', 'alpha_30', 'alpha_50', 'alpha_150', 'alpha_300', 'alpha_400']
    snt_df = pd.DataFrame.from_dict( sentiments, orient='index', columns=cols  )
    snt_df.to_csv( ARTICLE_SENTIMENTS )

    #plotting.sentiment_hist( snt_df, 'compound', SENTIMENT_HISTO) # This is not good for large texts
    hist_bins = 20
    plotting.sentiment_hist( snt_df, 'mean_sentence_compound', hist_bins, SENTIMENT_HISTO)

    '''
