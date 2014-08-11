
import nltk.data

from nltk.tag.stanford import NERTagger
from nltk.tag.stanford import POSTagger

from nltk.corpus import stopwords
from text import textelem as te

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
wnl = nltk.WordNetLemmatizer() 

punctuation = [',', '.', ':', ';', '?', '!']

def document_tokens(text, collocations = None):
    
    '''
    Tokenize the document
    
    :param text: text as string
    :param collocations: a list of collocations for the input text
    '''
    
    sentences = {}
    sentences_str = tokenizer.tokenize(text)
    for s in sentences_str:
        print s  
        st = sentence_tokens(s, collocations)
        sentences[st.id] = st
    
    d = te.Document(sentences, text)
    return d

def sentence_tokens(sentence, collocations = None):
    
    '''
    Tokenize the sentence
    
    :param sentence: a sentence as string
    :param collocations: a list of collocations for the input text
    '''
 
    # tokenize the sentence
    tokens_str = nltk.word_tokenize(sentence)
        
    # remove punctuation
    tokens_str = [t for t in tokens_str if t not in punctuation]
        
    # identify collocations
    # identify named entities
        
    # remove stop words
    filtered_tokens = [t for t in tokens_str \
                       if not t in stopwords.words('english')]

    # tokens pos
    tokens_pos = nltk.pos_tag(filtered_tokens)
        
    # create list of Token objects
    tokens = {}
    for token in tokens_pos:
        lemma = wnl.lemmatize(token[0])
        pos = token[1]
        word_str = token[0]
        t = te.Token(word_str, lemma, pos)
        tokens[t.id] = t
                
        print t
        
    sent = te.Sentence(tokens, sentence)
    return sent

def assign_concepts(kb_gr, doc):
    
    '''
    Assign concepts to tokens in the document
    
    :param kb_gr: knowledge base graph
    :param doc: the document
    :return: token_concepts: dictionary keyed on token_ids 
                             for each token id a list of knowledge base 
                             candidate concept ids and an annotation id is kept
    '''
    
    tokens = doc.tokens
    
    token_concepts = {}
    for token in tokens.values():
        concepts = kb_gr.concepts(token)
        a = te.Annotation(concepts)        
        token_concepts[token.id] = a
        
    return token_concepts

