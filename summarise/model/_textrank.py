import numpy as np
import networkx as nx
import spacy
from collections import OrderedDict
from spacy.lang.en.stop_words import STOP_WORDS
from summarise.preprocess import clean_tokens
from sklearn.metrics.pairwise import cosine_similarity

# SpaCy models
nlp = spacy.load('en_core_web_lg')

class KeywordTextRank():
    """Extract keywords from text"""
    
    def __init__(self):
        self.d = 0.85 # damping coefficient, usually is .85
        self.min_diff = 1e-5 # convergence threshold
        self.steps = 10 # iteration steps
        self.node_weight = None # save keywords and its weight

    
    def set_stopwords(self, stopwords):  
        """Set stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True
    
    def sentence_segment(self, doc, candidate_pos, lower):
        """Store those words only in cadidate_pos"""
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences
        
    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab
    
    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i+1, i+window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs
        
    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())
    
    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1
            
        # Get Symmeric matrix
        g = self.symmetrize(g)
        
        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm!=0) # this is ignore the 0 element in norm
        
        return g_norm

    
    def get_keywords(self, number=10):
        """Print top number keywords"""
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            print(key + ' - ' + str(value))
            if i > number:
                break
        
        
    def analyse(self, text, 
                candidate_pos=['NOUN', 'PROPN'], 
                window_size=4, lower=False, stopwords=list()):
        """Main function to analyze text"""
        
        # Set stop words
        self.set_stopwords(stopwords)
        
        # Pare text by spaCy
        doc = nlp(text)
        
        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower) # list of list of words
        
        # Build vocabulary
        vocab = self.get_vocab(sentences)
        
        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)
        
        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)
        
        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))
        
        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1-self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr))  < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]
        
        self.node_weight = node_weight

class SentenceTextRank():
    """Extract ranked sentences from text"""
    def __init__(self):        
        self.rows       = 0

    def create_sentence_vectors(self, doc, subract_mean=False):
        """ Creates mean sentence vectors"""
        sentences = list( doc.sents )
        sentence_vectors = []
        self.rows = sentences[0].vector.size
        for sentence in sentences:
            clean = filter(clean_tokens, sentence)
            clean_sentence = list(clean)
            n_tokens = len(clean_sentence)
            if n_tokens !=0:
                v = sum([t.vector for t in clean_sentence]) / n_tokens
            else:
                v = np.zeros((self.rows,))
            sentence_vectors.append(v)
        # Subtract mean vector
        if subract_mean == True:
            sentence_vectors = sentence_vectors - (sum(sentence_vectors) / len(sentences))
        return sentences, sentence_vectors
    
    def create_similarity_matrix(self, sentence_vectors):
        """Creates similarity matrix """
        
        n_sentences = len(sentence_vectors)
        similarity_matrix = np.zeros([n_sentences, n_sentences])
        for i in range(n_sentences):
            for j in range(n_sentences):
                if i != j:
                    similarity_matrix[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,self.rows), sentence_vectors[j].reshape(1,self.rows))[0,0]
        return similarity_matrix

    def analyse( self, text ):
        """Performs word embedding to caluclate sentence vectors and uses PageRank alogithm to rank sentences to use for summary
        Inputs
        ------
        text: string
            String containing document text

        Returns
        -------
        ranked_sentences : list
            List of sentences in descending ranked order
        
        """

        # Tokenise
        doc = nlp( text )

        # Create sentence vectors
        sentences, sentence_vectors = self.create_sentence_vectors( doc, subract_mean=False )

        # Create similarity matrix
        similarity_matrix = self.create_similarity_matrix( sentence_vectors )

        # Rank sentences
        nx_graph            = nx.from_numpy_array( similarity_matrix )
        scores              = nx.pagerank( nx_graph )
        ranked_sentences    = sorted(((scores[i],s) for i,s in enumerate( sentences )), reverse=True)
        return ranked_sentences