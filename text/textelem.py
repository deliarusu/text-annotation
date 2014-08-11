
import itertools

class Token:
    
    '''
    Token class
    
    id: token id
    word_str: string representation of the token
    lemma: token lemma
    pos: token part of speech 
    '''
    
    newid = itertools.count().next
     
    def __init__(self, word_str, lemma, pos):
        self.id = Token.newid()
        self.word_str = word_str
        self.lemma = lemma
        self.pos = pos  
        
    def __str__(self):
        t = (self.id, self.word_str, self.lemma, self.pos)
        return str(t)   
        
class Annotation:
    
    '''
    Annotation class
    
    candidate_concepts: a list of candidate concepts
    annotation_id: id of the annotation (index in the candidate concepts list)
    '''
    
    def __init__(self, candidate_concepts):
        self.candidate_concepts = candidate_concepts
        self.annotation_id = None
            
    
class Sentence:
    
    '''
    Sentence class
    
    id: sentence id
    tokens: dictionary keyed on token ids
    sentence_str: sentence as a string    
    '''
    
    newid = itertools.count().next
    
    def __init__(self, tokens, sentence_str):
        self.id = Sentence.newid()
        self.tokens = tokens
        self.sentence_str = sentence_str
        
class Document:
    
    '''
    Document class
    
    id: document id
    tokens: dictionary keyed on token ids
    sentences: dictionary keyed on sentence ids
    '''
    
    newid = itertools.count().next
    
    def __init__(self, sentences, text_str):
        self.id = Document.newid()
        self.sentences = sentences

        self.tokens = {}
        for s in self.sentences.values():
            t = s.tokens
            self.tokens = dict(t.items() + self.tokens.items())
