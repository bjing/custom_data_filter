import re

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
    
    def __init__(self, match_method):
        self.__match_method = match_method
        
    def find_match(self, data_factory, page_factory):
        self.__match_method(data_factory, page_factory)
        
       
def mass_page_match(data_factory, page_factory):
    """
    Forever
    """
    pattern = ".{0,30}%s.{0,30}"
    
    for data_record in data_factory.data:
        regex = re.compile(pattern % data_record)
        for page in page_factory.data:        
            html_text = '\n'.join(page['stripped_content'])
            results = regex.findall(html_text)
            
            for result in results:
                if page['should_match']:
                        print "Matched Keyword: %s" % data_record
                        print "Filename: %s" % page['file_name']
                        print "Context: %s\n" % result
                else:
                    print "False positive match"
        
        
def baseline_match(data_factory, page_factory):
    """
    real    0m16.906s
    user    0m16.784s
    sys    0m0.106s
    """
    pattern = ".{0,30}%s.{0,30}"
    
    for data_record in data_factory.data:
        regex = re.compile(pattern % data_record)
        for page in page_factory.data:                  
            for line in page['stripped_content']:
                if data_record in line:
                    if page['should_match']:
                        print "Matched Keyword: %s" % data_record
                        print "Filename: %s" % page['file_name']
                        m = regex.search(line)
                        print "Context: %s\n" % m.group(0)
                    else:
                        print "False positive match"
            
