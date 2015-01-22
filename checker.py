#!/usr/bin/env python

__version__ = 0.1

import os
import itertools
import functools
import glob
import re
import decorators
import abc

import html_parser



class Config:
    """
    A singleton class that holds all the configuration.
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
    
    
class Factory:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def data(self):
        pass

class Data_Factory(Factory):
    """
    """
    def __init__(self):
        # __data is a list of strings
        self.__data = None
        self.__normalised = False
        
    
    @property
    def data(self):
        if self.__data is None:
            self.__get_data_from_files()
            
        if not self.__normalised:
            self.__normalise_data()
        
        return self.__data
        
    
    def __get_data_from_files(self):
        """
        Get the corpus data from files
        
        Corpus is stored in an iterator 
        """
        
        def parse_data_file(file_):
            with open(file_, 'r') as fd:
                for line in fd:
                    line = line.strip()
                    if len(line):
                        yield line 
                
        # Get data file names  
        data_filenames = glob.glob(os.path.join(Config.data_path,Config.data_file_pattern))
        print "Data files: %s" % data_filenames
    
        # Parse each file
        data_tmp = map(parse_data_file, data_filenames)

        self.__data = [i.strip() for i in itertools.chain.from_iterable(data_tmp)]
        
    
    def __normalise_data(self):
        print "DEBUG: Normalising data"
                    
        # Change to all lower case
        self.__data = [ s.lower() for s in self.__data ]
        
        # Remove leading []
        self.__data = [ re.sub("^\s*\[.+\][^\w]\s*", "", s) for s in self.__data ]
        
        # Remove non-word chars
        # Define a partial function so we can use the map() function, which only accepts one
        # argument
        p_regex_sub = functools.partial(re.sub, "[\W]", " ")
        self.__data = map(p_regex_sub, iter(self.__data))
        
        # Remove leading and trailing spaces
        self.__data = [ s.strip() if len(s.strip()) > 15 else '' for s in self.__data ]
        self.__data = filter(lambda s: len(s) != 0, self.__data)
        
        self.__data = set(self.__data)
        
        self.__normalised = True
   

class Page_Factory(Factory):
    __pages = list()
    
    @property
    def data(self):
        if not self.__pages:
            self.__load_pages()
        
        return self.__pages

    def __load_pages(self):
        """
        Parse all html pages, preparing them for matching against the corpus
        
        Here we define a series of decorators for parsing the html pages. The reason why I design it 
        this way is that you can easily add or remove extra pre-processing steps by simply adding or
        removing the decorators for function parse_page()  
        """
    
        @decorators.handle_html_header
        def parse_page(file_name, html):
            """
            Parse an html page, removing all markups
            Handle first two lines through the html_header decorator
            """
            
            html_text = '\n'.join(html)
            
            # lower case
            html_text = html_text.lower()
            
            stripped_page = html_parser.strip_html_tags(html_text)
            # Strip html tags
            #p_regex_sub = functools.partial(re.sub, "<[^<]+?>", " ")
            #stripped_page = map(p_regex_sub, iter(html_lower))
            return stripped_page.split('\n')
            

        html_files = glob.glob(os.path.join(Config.data_path,Config.html_file_pattern))
        print html_files
        # Loop through all HTML files
        for file_ in html_files:
            # Read and parse page
            print "Processing html file %s" % file_
            with open(file_, 'r') as fd:
                #page = Page(*parse_page(fd))
                html = fd.readlines()
                self.__pages.append(parse_page(file_, html))
                
    
def find_match(data_factory, page_factory):
    
    #for data_record in data_factory.data:
    #    print data_record
        
    #for page in page_factory.data:
    #    #print page['html_content']
    #    print page['stripped_content']
        
    #return

    pattern = ".{0,30}%s.{0,30}"
    
    for data_record in data_factory.data:
        regex = re.compile(pattern % data_record)
        for page in page_factory.data:
            for line in page['stripped_content']:
                if data_record in line:
                    print "Matched Keyword: %s" % data_record
                    print "Filename: %s" % page['file_name']
                    
                    if page['should_match']:
                        
                        m = regex.search(line)
                        print "Context: %s\n" % m.group(0)
                    else:
                        print "False positive match"


def main():
    Config.show_config()
    
    data_factory = Data_Factory()
    page_factory = Page_Factory()
    
    find_match(data_factory, page_factory)


if __name__ == '__main__':
    main()