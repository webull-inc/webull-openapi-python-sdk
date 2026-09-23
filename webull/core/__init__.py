__version__ = '3.0.3'

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        """
        null handler
        """
        pass
    
logging.getLogger('webull.core').addHandler(NullHandler())
