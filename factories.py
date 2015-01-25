import abc
import os
import glob
import re
import functools
import itertools

import decorators
import html_parser
from config import Config
import utils

"""
    We define "factory" methods to generate the input data we need for matching
    
    These aren't traditional factory classes, but I named them this way just to 
    make sense.
"""

class Base_Factory:
    """
    Base factory class that enforces the interface Class.data.
    """    
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def data(self):
        pass

class Data_Factory(Base_Factory):
    """
    This class is responsible for generating the corpus data that we want to
    match in html pages
    
    It makes sure whenever the data attribute is initialised, the __normalised()
    method gets invoked.
    """
    def __init__(self):
        # __data is an iterator of strings
        self.__data = None
        self.__normalised = False
        
        self.logger = utils.get_logger(__name__)
        
    @property
    def data(self):
        """
        A getter method that return corpus data
        
        The corpus data gets normalised if it hasn't already 
        
        :returns: the corpus data
        :rtypes: iterator of strings
        """
        if self.__data is None:
            self.__get_data_from_files()
            
        if not self.__normalised:
            self.__normalise_data()
        
        return self.__data
        
    
    def __get_data_from_files(self):
        """
        Get the corpus data from files and store the data in __data
        """    
        def parse_data_file(file_):
            """
            A function for parsing each file
            
            :returns: an iterator that has each line as an item
            :rtype: iterator of strings
            """
            with open(file_, 'r') as fd:
                for line in fd:
                    line = line.strip()
                    if len(line):
                        yield line 
                
        # Get data file names  
        data_filenames = glob.glob(os.path.join(Config.data_path,Config.data_file_pattern))
        self.logger.debug("Data files: %s" % data_filenames)
    
        # Parse each file
        data_tmp = map(parse_data_file, iter(data_filenames))

        # Each file is represented as an iterator of strings. We chain the 
        # iterators up
        self.__data = itertools.chain.from_iterable(data_tmp)
        
    def __normalise_data(self):
        self.logger.info("Normalising corpus data")
                    
        # Change to all lower case
        self.__data = (s.lower() for s in self.__data)
        
        # Remove leading []
        self.__data = (re.sub("^\s*\[.+\][^\w]\s*", "", s) for s in self.__data)
        
        # Remove non-word chars
        # Define a partial function so we can use the map() function, which 
        # only accepts one argument
        p_regex_sub = functools.partial(re.sub, "[\W]+", " ")
        self.__data = map(p_regex_sub, self.__data)
        
        # Remove leading and trailing spaces
        self.__data = (s.strip() if len(s.strip()) > 15 else '' for s in self.__data)
        
        # Throw away empty lines
        self.__data = filter(lambda s: len(s) != 0, self.__data)
        
        # De-duplicate the corpus data using a set
        # Then convert it back to an iterator
        self.__data = iter(set(self.__data))
        
        # Flag that the corpus data has been normalised
        self.__normalised = True
        
    def dump_data_to_file(self, path):
        filename = os.path.join(Config.root, path)
        filename = os.path.join(filename, 'processed.dat')
        self.logger.info("Dumping processed corpus data to file %s" % filename)
        with open(filename, 'w') as fd:
            fd.write('\n'.join(self.data))
   
class Page_Factory(Base_Factory):
    """
    A page factory that produces pages to match against
    Change parse_html_page() if it's other page format
    """
    
    # __pages is a list of dictionaries
    __pages = list()
    
    def __init__(self):
        self.logger = utils.get_logger(__name__)
    
    @property
    def data(self):
        if not self.__pages:
            self.__load_pages()
        
        return self.__pages

    def dump_stripped_to_file(self, path):
        """
        Dump stripped html data to file for debugging purpose
        """
        for page in self.data:
            filename = os.path.join(Config.root, path)
            filename = os.path.join(filename, os.path.basename(page['file_name']))
            self.logger.info("Creating stripped file for %s" % page['file_name'])
            with open(filename, 'w') as fd:
                fd.write('\n'.join(page['stripped_content']))

    def __load_pages(self):
        """
        Parse all pages, preparing them for matching against the corpus
        
        Here we define a decorators for parsing the html pages' first two lines. 
        The reason why I design it this way is that you can easily add or remove 
        extra processing steps by simply adding or removing decorators
        """
    
        @decorators.handle_html_header
        def parse_html_page(file_name, html):
            """
            Parse an html page, removing all markups
            Handle first two special lines through the html_header decorator
            
            :param file_name: name of the html file
            :type file_name: str
            :param html: raw html content
            :type html: list of str
            
            :returns: html content with markups stripped
            :rtype: list of str
            """
            
            html_text = '\n'.join(html)
                        
            # Strip all HTML markups
            stripped_page = html_parser.strip_html_tags(html_text)
            
            # lower case
            stripped_page = stripped_page.lower()
            
            # Remove all non-word characters. Since removing non-word characters will remove
            # \n, we apply this to each line instead of the whole html text
            stripped_page = stripped_page.split('\n') 
            p_regex_sub = functools.partial(re.sub, "[\W]+", " ")
            stripped_page = map(p_regex_sub, stripped_page)
            
            # Remove leading and trailing spaces for each line
            stripped_page = [line.strip() for line in stripped_page]
            # Filter out empty lines
            stripped_page = filter(lambda line: len(line) != 0, stripped_page)
            
            return stripped_page
            
        # Process all html files
        html_files = glob.glob(os.path.join(Config.data_path,Config.html_file_pattern))
        
        # Loop through all HTML files
        for file_ in html_files:
            # Read and parse page
            self.logger.info("Processing html file %s" % file_)
            with open(file_, 'r') as fd:
                html = fd.readlines()
                self.__pages.append(parse_html_page(file_, html))
               
