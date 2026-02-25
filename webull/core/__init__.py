__version__ = '2.0.0'

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        """
        null handler
        """
        pass
    
logging.getLogger('webull.core').addHandler(NullHandler())
