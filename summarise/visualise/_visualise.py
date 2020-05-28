import spacy
from spacy import displacy
from spacy.matcher import Matcher
from itertools import compress
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt 
from PIL import Image
import seaborn as sns
import pandas as pd
import numpy as np
import os.path
import re
import math

nlp     = spacy.load("en_core_web_lg")    

def plot_histogram( tokens, n_tokens=15 ):
    """Plots histogram of tokens
    Parameters
    ----------
    tokens : list
        List containing tokens that will be turned into a histogram
    
    n_tokens : integer
        Top n tokens to display

    Returns
    -------
    plt : figure object
    """
    # Count of appearances of each word
    token_count_df = count_tokens( tokens ).reset_index()
    token_count_df.columns = ['Tokens','Counts']

    # Plot histogram
    plt.figure( figsize = (3, 6), facecolor = None )
    sns.set( style="whitegrid" )
    sns.barplot( 
        x="Counts", 
        y="Tokens", 
        data=token_count_df.head( n_tokens ),
        palette="Blues_d"   
        )
    # Show
    plt.show() 

    return plt

def count_tokens( tokens ):
    """Counts frequency of tokens
    Parameters
    ----------
    tokens : list
        List containing tokens that will be counted   

    Returns
    -------
    token_count_df : pandas.Dataframe
        Dataframe containing columns ['Tokens', 'Counts']
    """
    # Convert to dataframe
    token_df = pd.DataFrame( tokens, columns=['Tokens'] )
    # Count of appearances of each word
    token_count_df = token_df.groupby( 'Tokens' ).size()\
                                            .reset_index( name='Counts' )\
                                            .sort_values( 'Counts', ascending=False )\
                                            .reset_index( drop=True )    
    token_count_df = token_count_df.set_index('Tokens')     
    return token_count_df

def count_document_tokens( documents ):
    """Counts frequency of tokens over several documents and returns merged table
    Parameters
    ----------
    documents : list
        List containing documents

    Returns
    -------
    document_token_count_df : pandas.Dataframe
        Dataframe containing columns ['Tokens', 'Counts'] indexed by document
    
    """    
    token_counts = [ count_tokens( document ).Counts for document in documents ]
    document_token_count_df = pd.concat(token_counts, axis=1, ignore_index=False)    
    return document_token_count_df

def plot_wordcloud( tokens, mask_image="", filename="" ):
    """Plots wordcloud of tokens
    Parameters
    ----------
    tokens : list
        List containing tokens that will be plotted   

    mask_image : string
        path to mask image

    Returns
    -------
    plt : figure object
    
    """

    # Concatinate list into single string
    clean_text = ""
    clean_text += " ".join(tokens)+" "

    if os.path.isfile( mask_image ):
        mask            = np.array( Image.open ( mask_image ) )
        image_colors    = ImageColorGenerator( mask )
        wordcloud = WordCloud(
                        width = 1200, 
                        height = 1200, 
                        background_color = 'black',  
                        mask=mask,              
                        min_font_size = 10).generate(clean_text)
    else:
        wordcloud = WordCloud(
                    width = 1200, 
                    height = 1200, 
                    background_color = 'black',                        
                    min_font_size = 10).generate(clean_text)

    # Save WordCloud
    if len(filename) > 0:
        wordcloud.to_file(filename)
    
    # plot the WordCloud image                        
    plt.figure( figsize = (8, 8), facecolor = None ) 
    plt.imshow( wordcloud, interpolation="bilinear" ) 
    plt.axis( "off" ) 
    plt.tight_layout( pad = 0 ) 
    # Show
    plt.show() 

    return plt

    # store to file
    # plt.savefig("img/wordcloud.png", format="png")

def highlight_entities( text, n_lines=float("Inf") ):   
    """Displays entities identified by spaCy    
    Parameters
    ----------
    text : string
        Document string

    n_lines : integer
        Number of lines to display

    Returns
    -------    
    N/A
    
    """    
    if math.isfinite( n_lines ):
        lines   = text.splitlines()        
        n       = len(lines)
        assert( n <= n_lines, "Number of lines must be less than equal to number of lines in text [{}].".format(n) )
        lines   = lines[0:(n_lines-1)]
        text    = "\n".join( lines )
    doc     = nlp( text )
    displacy.render(doc, style="ent")

    return

def count_entities( document ):
    """Counts frequency of entities
    Parameters
    ----------
    document : string
        String containing document text

    Returns
    -------
    token_count_df : pandas.Dataframe
        Dataframe containing columns ['Tokens', 'Types', 'Counts']
    """

    matcher = Matcher(nlp.vocab, validate=True)
    # Define patterns
    organsiation    = [{"ENT_TYPE": "ORG", "POS": "PROPN"},{"ENT_TYPE": "ORG", "OP": "*"} ]
    person          = [{"ENT_TYPE": "PERSON", "POS": "PROPN"}, {"ENT_TYPE": "PERSON", "OP": "+"}]
    # Add match patterns
    matcher.add( "Organisation", None, organsiation )
    matcher.add( "Person", None, person )
    # Analyse document
    doc     = nlp( document )
    matches = matcher(doc)
    # Extract matches
    types       = []
    start_index = []
    end_index   = []
    substrings  = []
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        types.append( string_id )
        start_index.append( start )
        end_index.append( end )
        substrings.append( span.text )
    # Apply "greedy" logic
    s   = np.array(start_index)
    e   = np.array(end_index)
    ok  = s > 0
    for i, (start, end) in enumerate( zip( s, e ) ):
        # Is token part of a larger span elsewhere in the list?
        is_substr   = np.logical_or( np.logical_and(s > start, e <= end ), np.logical_and(s >= start, e < end ) )
        # Remove substrings
        ok = np.logical_and( ok, ~is_substr )
    types           = list(compress(types, ok))
    substrings      = list(compress(substrings, ok))
    # Generate dataframe
    entities_df = pd.DataFrame({'Types':types, 'Tokens':substrings})
    entities_df = entities_df.set_index('Tokens')
    entities_df = entities_df.reset_index(drop=True, inplace=True)
    counts_df   = count_tokens( substrings )
    return pd.concat([counts_df, entities_df], axis=1, join='inner')

# Formatting
def set_background(colour, text):
    """Sets text background colour in shell. Returns plain if colour doesn't exist.
    
    Parameters
    ----------
    text : string
        Document string

    colour : string
        black|red|green|yellow|blue|magenta|cyan|gray

    Returns
    -------    
    text : string
        String with formatting tags
    """
    if colour == "black":
        return "\033[1;40m" + str(text) + "\033[0m"
    if colour == "red":
        return "\033[1;41m" + str(text) + "\033[0m"
    if colour == "green":
        return "\033[1;42m" + str(text) + "\033[0m"
    if colour == "yellow":
        return "\033[1;43m" + str(text) + "\033[0m"
    if colour == "blue":
        return "\033[1;44m" + str(text) + "\033[0m"
    if colour == "magenta":
        return "\033[1;45m" + str(text) + "\033[0m"
    if colour == "cyan":
        return "\033[1;46m" + str(text) + "\033[0m"
    if colour == "gray":
        return "\033[1;47m" + str(text) + "\033[0m"
    return str(text)

def set_foreground(colour, text):
    """Sets text foreground colour in shell. Returns plain if colour doesn't exist.
    
    Parameters
    ----------
    text : string
        Document string

    colour : string
        black|red|green|yellow|blue|magenta|cyan|gray

    Returns
    -------    
    text : string
        String with formatting tags
    """
    if colour == "black":
        return "\033[1;30m" + str(text) + "\033[0m"
    if colour == "red":
        return "\033[1;31m" + str(text) + "\033[0m"
    if colour == "green":
        return "\033[1;32m" + str(text) + "\033[0m"
    if colour == "yellow":
        return "\033[1;33m" + str(text) + "\033[0m"
    if colour == "blue":
        return "\033[1;34m" + str(text) + "\033[0m"
    if colour == "magenta":
        return "\033[1;35m" + str(text) + "\033[0m"
    if colour == "cyan":
        return "\033[1;36m" + str(text) + "\033[0m"
    if colour == "gray":
        return "\033[1;37m" + str(text) + "\033[0m"
    return str(text)
    
def highlight_str( text, substring ):
    """Sets substring foreground color to black and background to yellow. Returns formatted string.
    Use print( text ) to view result.
    """
    return re.sub( substring, set_foreground( 'black', set_background("yellow",'\g<0>') ), text )