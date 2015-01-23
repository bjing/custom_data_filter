import os

class Config:
    """
    A singleton class that holds all the configuration.
    
    I would have config files on disk if the configuration isn't just a few 
    values like below.
    """
    root = os.path.dirname(__file__) 
    data_path = os.path.join(root, 'data')
    data_file_pattern = '*.dat'
    html_file_pattern = '*.html'
    
    @classmethod
    def show_config(cls):
        """
        Show config info
        """
        print "================================="
        print "Root path: %s " % Config.root
        print "Data path: %s " % Config.data_path
        print "Data file pattern: %s " % Config.data_file_pattern
        print "================================="
    
    
 