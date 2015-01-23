import logging
from config import Config

def get_logger(logger_name, **kwargs):
    """
    Get a logger object
    
    :param logger_name: name of the logger
    :type logger_name: str
    :returns: a logger for logging
    :rtype: Logger object 
    """
    # create logger
    logger = logging.getLogger(logger_name)
    if kwargs.has_key('default_logging_level'):
        logger.setLevel(kwargs['default_logging_level'])
    else:
        logger.setLevel(Config.default_logging_level)
    
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if kwargs.has_key('log_file'):
        fh = logging.FileHandler(kwargs['log_file'])
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)    
        
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger
