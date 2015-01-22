#!/usr/bin/env python

__version__ = 0.1

import os
import itertools
import re
import decorators

class Config:
    """
    A singleton class that holds all the configuration.
    """
    root = os.path.dirname(os.path.dirname(__file__)) 
    data_path = os.path.join(root, 'data')
    data_file_ext = 'dat'
    html_file_ext = 'html'
    exclusion_file = os.path.join(data_path, 'exclusions.txt')
    
    
def show_config():
    """
    Show config info
    """
    print "Root path: %s " % Config.root
    print "Data path: %s " % Config.data_path
    print "Exclusion_file: %s " % Config.exclusion_file
    print "Data file extention: %s " % Config.data_file_ext
        

## TODO put these data retrieval functions in a factory
def get_data():
    """
    Get the corpus
    
    Corpus is stored in an iterator 
    """
    def parse_file(file_):
        """
        Parse a data file and return a generator function of all the records 
        A tuple contains tokens from a line
        
        :param file_: the file
        :type file_: file descriptor 
        :returns: an iterator of the parsed data 
        :rtype: iterator of tuples 
        """
        def parse_line(line):
            """
            Parse a single line of the corpus file
            
            :param line: a single line read from the corpus file
            :type line: string
            :returns: a list of tokens
            :rtype: list
            """
            line = line.strip().lower()
            if len(line) != 0:
                try:
                    # Lots of sites remove the extension from files, so dump ours if we need to
                    line = re.sub("\..{3,5}$", "", line)
                    # Remove leading and trailing brackets
                    line = re.sub("\s*\[.+\]\s*-\s*", "", line)
                    line = re.sub("\s*\[.+\]$", "", line)
                    res = re.split("\s{3,}", line)
                    if len(res) < 3:
                        res = []
                    else:
                        res[2] = res[2].strip(' ')
                        if len(res[2].strip(' ')) < 10:
                            res = []
                        else:
                            res[2] = res[2].strip(' ').lstrip('.')
                            #res[2] = res[2].decode("utf-8").encode('ascii', 'ignore')
                            
                        #print res
                    return res
                    
                except IndexError as e:
                    print "Error: {0} for line {1}".format(e, line)
        
        return [parse_line(line) for line in file_]


    # Get data file names by creating a filter and picking up file names that 
    # end with Config.data_file_ext
    data_files = filter(lambda f: f.endswith(Config.data_file_ext), 
                        map(lambda f: os.path.join(Config.data_path, f), os.listdir(Config.data_path)))

    # Open a file descriptor for each file and return an iterator of all file descriptors
    fds = (open(data_file, 'r') for data_file in data_files)
    # Parse each file and chain the iterator results together
    data = map(parse_file, fds)
    # Close file descriptors
    for fd in fds:
        fd.close()
    
    return [line for file_ in data for line in file_]

def get_exclusions():
    """
    A generator function that gets all the re filters from the exclusions.txt file
    
    :returns: an iterator that has all the exclusion rules
    :rtype: iterator
    """
    exclusions = []
    with open(Config.exclusion_file, 'r') as fd:
        for line in fd:
            line = line.rstrip()
            if line:
                exclusions.append(line)
                
    return exclusions

def parse_pages(data, exclusions):
    """
    Parse all html pages, preparing them for matching against the corpus
    
    Here we define a series of decorators for parsing the html pages. The reason why I design it 
    this way is that you can easily add or remove extra pre-processing steps by simply adding or
    removing the decorators for function parse_page()  
    """

    @decorators.handle_html_header
    def parse_page(html_fd):
        """
        Parse an html page, removing all markups
        Handle first two lines through the html_header decorator
        """
        stripped_page = re.sub('<[^<]+?>', '', ''.join(html_fd))
        return stripped_page
        
    html_files = filter(lambda f: f.endswith(Config.html_file_ext), 
                        map(lambda f: os.path.join(Config.data_path, f), os.listdir(Config.data_path)))

    # Loop through all HTML files
    for file_ in html_files:
        # Read and parse page
        print "Processing html file %s" % file_
        with open(file_, 'r') as fd:
            res = parse_page(fd)

        # Hash match
        for data_record in data:
            
            if not len(data_record):
                continue
            match = find_hash_match(data_record[2], data_record[1], exclusions, *res)
            if match:
                if res[1]:
                    print "Looking at data record: %s" % data_record
                    print "Found hash match of '{0}' on page {1}. Hash {2}".format(data_record[2], res[0], data_record[1])
        
        unique_names = set([i[2] for i in data if len(i) == 3 ])
        # Name match
        for name in unique_names:
            
            #print "Looking at data record: %s" % data_record
            #print data_record
            match = find_name_match(name, exclusions, *res)
            
            if match:
                if res[1]:
                    print "Looking at name record: %s" % name
                    print "Found name match of '{0}' on page {1}".format(name, file_)#res[0])
            #else:
                #print "%s didn't match (and should not have)" % res[0]

def find_hash_match(name, hash_, exclusions, source_url,should_match, html_page, stripped_page):
    # Check hash
    if hash_ in stripped_page:
        #print "Hash match: %s" % hash_
        return True
    
#@decorators.ignore_exclusions
def find_name_match(name, exclusions, source_url, should_match, html_page, stripped_page):
    # make all lower case
    stripped_page = stripped_page.lower()
    html_page = html_page.lower()
    
    for exclusion in exclusions:
        try:
            result = re.match(exclusion, name)
            return False
        except Exception as e:
            #print "Exclusion rule error: {0}:{1}".format(e, exclusion)
            pass
        
    # After hash match, we don't need hash anymore, 
    if name in html_page:
        #print "Name match: %s" % name
        return True

def main():
    show_config()
    data = get_data()
    exclusions = get_exclusions()
    
    parse_pages(data, exclusions)


if __name__ == '__main__':
    main()