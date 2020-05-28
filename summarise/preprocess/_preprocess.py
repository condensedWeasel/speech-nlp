# Import libraries
import re
import spacy
from sklearn.base import TransformerMixin

# Constants
INLINE_REF  = '(?<=[a-zA-Z][,\.”\'\"])[0-9]{1,2}|(?<=[a-zA-Z])[0-9]{1,2}(?=[,\.])'
PAGE_NOS    = r'[\r\n][0-9]{1,2}[ ]?[\r\n]'
FOOTER      = '(All speeches are available online at www.bankofengland.co.uk/publications/Pages/speeches/default.aspx )|(All speeches are available online at www.bankofengland.co.uk/news/speeches )'
REFERENCE   = r'[\r\n]{1,2}[0-9]{1,2}[ ]*[\"“\']?[a-zA-Z]{1}\w+.*(?=[\r\n]{1})'

# Text cleaning functions
def remove_artifacts( text ):
    """Removes inline references, page numbers and footers. Note: Must be run before remove_whitespace
    
    Parameters. 
    ----------
    text : string
        String containing text from the document

    Returns
    -------
    text : string
        Cleaned text
    """
    # Remove inline references e.g. foo[1]
    text = re.sub( INLINE_REF, '', text )
    # Remove page numbers \n[1]\n
    text = re.sub( PAGE_NOS, '', text )
    # Remove footer (url)
    text = re.sub( FOOTER, '', text )
    # Remove references
    text = re.sub( REFERENCE, '', text )
    return text

def remove_whitespace( text, remove_all=True ):
    """Removes repeated newline characters from document
    Parameters
    ----------
    text : string
        String containing text from the document

    Returns
    -------
    text : string
        Cleaned text
    """
    if remove_all:
        # Replace all whitespace (including newline characters) with space
        text = re.sub( r'\s+', ' ', text )
    else:
        # Replace blank lines with newline characters
        text = re.sub( r'\n[ \t\r\f\v]+', '\n', text )
        # Replace repeated newline charactes with single new line
        text = re.sub( r'[\n\r]+', '\n', text )
        # Replace repeated non-newline characters
        text = re.sub( r'(?:(?![\n\r])\s)+', ' ', text )
        
    return text

def clean_text( text ):
    """Wrapper function for remove_artifacts & remove_whitespace

    Parameters
    ----------
    text : string
        String containing text from the document

    Returns
    -------
    clean : string
        Cleaned text
    """
    text    = remove_artifacts(text)
    clean   = remove_whitespace(text)
    return clean

# Custom class for cleaning data
class cleaner(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        return [clean_text(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}

def clean_tokens( token, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'] ):
    """Returns list True / False according to whether token is clean / dirty
    
    Parameters
    ----------
    token : spacy.tokens.token.Token
        String containing text from the document
    
    allowed_postags : list
        List of parts of speech tags

    Returns
    -------
    tf : bool
        Flag set to true if token is clean

    """ 
    return token.is_alpha and not( token.is_stop ) and \
            token.pos_ in allowed_postags

# Use spacy to tokenise documents
def tokeniser( document, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'] ):
    """Returns list of tokens from document
    
    Parameters
    ----------
    document : string
        String containing text from the document
    
    allowed_postags : list
        List of parts of speech tags

    Returns
    -------
    text : list
        Tokenised document

    """ 
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(document)
    #Generate clean list of tokens
    tokens = []
    for word in doc:
        if word.is_alpha and not( word.is_stop ) and \
            word.pos_ in allowed_postags:
            tokens.append( word.lemma_.lower() ) 
    return tokens

def find_references( text ):
    """Finds references in text

    Parameters.
    ----------
    text : string
        String containing text from the document

    Returns
    -------
    tokens : list
        Matched tokens
    """
    tokens = re.findall(REFERENCE, text)
    return tokens