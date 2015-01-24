import re
import utils

"""
    This strategy pattern is mainly written for me to test different matching
    methods that I had in mind.
    
    The Strategy class gives a unified interface to invoke matching
    
    Different matching methods can be defined as function in this file and 
    initialise an instance of Strategy() class with the method name as an 
    argument to the constrctor, 
    
    Example:
        a_strategy = Strategy(a_match_method)
        a_strategy.find_match(*args)
        
"""

class Strategy:
    """
    The strategy class provides a unified interface for starting the matching
    process depending on what matching method the user chooses 
    
    It is probably a bit of an overkill in this case. But for program of 
    larger size this would make things more manageable.
    """
    
    def __init__(self, match_method):
        self.__match_method = match_method
        
        self.__logger = utils.get_logger(__name__)
        
    def find_match(self, data_factory, page_factory):
        """
        This is the method for starting the match process
        
        Depending on how __match_method is initialised, different match
        methods can be executed here
        """
        self.__match_method(data_factory, page_factory, self.__logger)
        
       
def mass_page_match(data_factory, page_factory, logger):
    """
    This method treats each stripped html page as a big string and searches 
    for the data we want to match
    
    This takes forever, never bothered to wait until it finishes
    """    
    
    pattern = ".{0,30}%s.{0,30}"
    
    for data_record in data_factory.data:
        regex = re.compile(pattern % data_record)
        for page in page_factory.data:        
            html_text = '\n'.join(page['stripped_content'])
            results = regex.findall(html_text)
            
            for result in results:
                if page['should_match']:
                        logger.info("Matched Keyword: %s" % data_record)
                        logger.info("Filename: %s" % page['file_name'])
                        logger.info("Context: %s\n" % result)
                else:
                    logger.warn("False positive match")
        
        
def baseline_match(data_factory, page_factory, logger):
    """
    My baseline, looping through keywords in outter loop, and looping through pages in inner loop.
    Within the inner loop, we loop through every line of each html file to do the matching
    """
    pattern = ".{0,30}%s.{0,30}"
    
    for data_record in data_factory.data:
        regex = re.compile(pattern % data_record)
        for page in page_factory.data:                  
            for line in page['stripped_content']:
                if data_record in line:
                    if page['should_match']:
                        logger.info("Matched Keyword: %s" % data_record)
                        logger.info("Filename: %s" % page['file_name'])
                        m = regex.search(line)
                        logger.info("Context: %s\n" % m.group(0))
                    else:
                        logger.warn("False positive match")
            
