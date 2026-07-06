__version__ = '2.0.13'

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        """
        null handler
        """
        pass
    
logging.getLogger('webull.core').addHandler(NullHandler())
