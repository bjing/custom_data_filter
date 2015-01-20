#!/usr/bin/env python3

import os
import itertools
import re

class Config:
    """
    A singleton class that holds all the configuration.
    """
    root = os.path.dirname(os.path.dirname(__file__)) 
    data_path = os.path.join(root, 'data')
    data_file_ext = 'dat'
    exclusion_file = os.path.join(data_path, 'exclusions.txt')
    
    
def show_config():
    """
    Show config info
    """
    print "Root path: %s " % Config.root
    print "Data path: %s " % Config.data_path
    print "Exclusion_file: %s " % Config.exclusion_file
    print "Data file extention: %s " % Config.data_file_ext
        

def get_data():
    
    def parse_file(file_):
        """
        Parse a data file and return a generator function of all the records 
        A tuple contains tokens from a line
        """
        def parse_line(line):
            line = line.strip()
            if len(line) != 0:
                try:
                    return re.split('\s+', line)
                except IndexError as e:
                    print "Error: {0} for line {1}".format(e, line)
        
        return (parse_line(line) for line in file_)


    # Get data file names by creating a filter and picking up file names that 
    # end with Config.data_file_ext
    data_files = filter(lambda f: f.endswith(Config.data_file_ext), 
                        map(lambda f: os.path.join(Config.data_path, f), os.listdir(Config.data_path)))

    # Open a file descriptor for each file and return an iterator of all file descriptors
    fds = (open(data_file, 'r') for data_file in data_files)
    # Parse each file and chain the iterator results together
    data = itertools.chain.from_iterable(map(parse_file, fds))
    # Close file descriptors
    for fd in fds:
        fd.close()
    
    return data

def get_exclusions():
    """
    A generator function that gets all the re filters from the exclusions.txt file
    """
    with open(Config.exclusion_file, 'r') as fd:
        for line in fd:
            yield line

def main():
    show_config()
    get_data()
    filter = get_exclusions()

if __name__ == '__main__':
    main()