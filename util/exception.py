
class UtilException(Exception):
    
    '''
    Exception class for this project.

    Attributes:
        expr -- input expression in which the exception occurred
        msg  -- explanation of the exception
    '''

    module = ''

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
        
    def __str__(self):
        
        s = ' '.join(self.module, str(self.expr), self.msg)
        return repr(s)

class GraphException(UtilException):
    
    '''
    Exception raised for the graph module.
    '''
    
    module = 'Graph'
    
    
class RelatednessException(UtilException):
    
    '''
    Exception raised for the relatedness module.
    '''
    
    module = 'Relatedness'    
    
class BowException(UtilException):
    
    '''
    Exception raised for the BOW module.
    '''
    
    module = 'BOW'
    
class AnnotationException(UtilException):
    
    '''
    Exception raised for the annotation module.
    '''
    
    module = 'Annotation'