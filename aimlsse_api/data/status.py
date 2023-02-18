from enum import Enum

class QueryStates(str, Enum):
    PROCESSED   = 'processed'
    '''Data has been processed and can be removed from storage, if necessary'''
    AVAILABLE   = 'available'
    '''Data is available in storage'''
    INCOMPLETE  = 'incomplete'
    '''Data is not yet available in storage, but the download is partially complete'''
    PENDING     = 'pending'
    '''Data is not in storage but online - a request has already been made'''
    NEW         = 'new'
    '''The request is new and has not yet been processed'''
    UNAVAILABLE = 'unavailable'
    '''Data is not in storage and not online'''
    INVALID     = 'invalid'
    '''Identifier does not relate to any data'''