
import numpy as np

MEDIAN = 'median'
AVERAGE = 'average'

def annotate_token(current_token_id, window_tokens, \
                   token_concepts, relatedness, rel_concepts):
    
    '''    
    Annotate the tokens in a given token window.
    
    :param current_token_id: token to be annotated
    :param window_tokens: the tokens (their ids) in a window to annotate
    :param token_concepts: dictionary of concept objects 
                           associated with the tokens 
    :param relatedness: relatedness object 
    :param rel_concepts: relatedness scores in the context window
    '''
        
    for token_id in window_tokens:
        
        compare_concepts = []
        annotation_id = token_concepts[token_id].annotation_id
        
        # if the token was not annotated, add all candidate concepts
        # else add the concepts found as a valid annotation
        if annotation_id == None:
            compare_concepts = token_concepts[token_id].candidate_concepts
        else:
            ann = token_concepts[token_id].candidate_concepts[annotation_id]
            compare_concepts.append(ann)
    
        max_rel = -1
        max_idx = 0
        
        for wconcept in compare_concepts:
            for idx, cconcept in \
            enumerate(token_concepts[current_token_id].candidate_concepts):
                
                rel = -1
                try:
                    # relatedness
                    rel = relatedness.compute(wconcept, cconcept)
                except:
                    pass
                
                if rel > max_rel:
                    max_rel = rel
                    max_idx = idx
                    
                rel_concepts[idx].append(rel)        
                
    token_concepts[current_token_id].annotation_id = max_idx   
       
 
def distrib(aggregation, rel_concepts, token_concept):
    
    '''
    :param aggregation: type of aggregation for the relatedness score
           currently either 'average' or 'median'
    :param rel_concepts: the relatedness scores to aggregate
    :param token_concept: the token for which to aggregate the 
           relatedness score 
    '''
    
    all_agg = []
    for c in rel_concepts:
        #print i
        c = np.array(c)
        
        agg = -1
        if aggregation == MEDIAN: 
            agg = np.median(c)
        elif aggregation == AVERAGE:  
            agg = np.average(c)
        
        all_agg.append(agg)
    
    all_agg = np.array(all_agg)
    max_rel = all_agg.max()
    max_idxs = [idx for idx, val in enumerate(all_agg) if val == max_rel] 
    
    token_concept.annotation_id = max_idxs[0]
    
   
         
                