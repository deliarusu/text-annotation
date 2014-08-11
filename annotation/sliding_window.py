
from util import exception
import annotate

def find_window_tokens(tokens, current_token_idx, window_start, window_size):
    
    '''
    
    Window tokens for the estimation position. Duplicate tokens are 
    considered only once. 
    
    :param tokens: list of text tokens
    :param current_token_idx: the current token index
    :param window_start: index of the token at the 
                         beginning of the sliding window 
    :param window_size: size of the sliding window
    
    :return: a list of token ids in that window
    
    '''
        
    window_tokens = []
    unique_tokens = []
    
    unique_tokens.append(tokens[current_token_idx].lemma)
    
    # look for candidate tokens in [window_start, len(tokens)] 
    token_idx = window_start
    while len(window_tokens) < window_size and token_idx < len(tokens):
        if not(tokens[token_idx] in unique_tokens) and \
            token_idx != current_token_idx:
            
            window_tokens.append(tokens[token_idx].id)
            unique_tokens.append(tokens[token_idx].lemma)
        token_idx += 1
                    
    # if not enough tokens 
    # look for candidate tokens in [0, window_start - 1] 
    token_idx = window_start - 1
    while len(window_tokens) < window_size and token_idx >= 0:
        if not(tokens[token_idx] in unique_tokens) and \
            token_idx != current_token_idx:
            
            window_tokens.append(tokens[token_idx].id)
            unique_tokens.append(tokens[token_idx].lemma)
        token_idx -= 1
                    
    return window_tokens
    

def wsd(tokens, token_concepts, window_size, relatedness):
    
    '''
    Assign concepts to text tokens using a sliding window algorithm
    
    :param tokens: list of text tokens
    :param token_concepts: dictionary keyed on token_ids 
                           for each token id a list of knowledge base 
                           candidate concept ids and an annotation id is kept
    :param window_size: the size of the sliding window
    :param relatedness: the relatedness object
    '''
    
    if len(tokens) < window_size:
        raise exception.AnnotationException(window_size, \
            'Window size should be less than the number of text ' \
            'tokens')
    elif len(tokens) < 1:
        raise exception.AnnotationException(len(tokens), \
            'No tokens in text')
    elif window_size < 2 or window_size % 2 != 0:
        raise exception.AnnotationException(window_size, \
            'Window size should be > 2 and an even number')
    
    window_start = 0
    window_end = window_start + window_size
    current_token_idx = window_start
    
    while current_token_idx < len(tokens):
        print current_token_idx
        
        token_id = tokens[current_token_idx].id
        if len(token_concepts[token_id].candidate_concepts) > 1:
            window_tokens = find_window_tokens(tokens, current_token_idx, \
                                               window_start, window_size)
            
            # annotate
            rel_concepts = [ [] for _ in range(0, \
                len(token_concepts[token_id].candidate_concepts))]
            annotate.annotate_token(token_id, window_tokens, \
                                    token_concepts, relatedness, rel_concepts)
            
            # aggregate relatedness scores using 'median' or 'average'
            if relatedness.aggregation != None:
                annotate.distrib(relatedness.aggregation, rel_concepts, \
                                 token_concepts[token_id])
            
        elif len(token_concepts[token_id].candidate_concepts) == 1:
            token_concepts[token_id].annotation_id = 0
    
    
        # update sliding window positions
        current_token_idx += 1
        reached_end = True
        if window_end < len(tokens) - 1 and \
            current_token_idx - window_start > window_size/2:
            window_end += 1
            reached_end = False
        if reached_end == False and window_end - window_start > window_size:
            window_start += 1          
