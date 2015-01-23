import functools
import re

"""
Decorators for data parsing and processing
"""
def handle_html_header(func):
    """
    A decorator that handles our special kind of html file, 
    which has first two lines reserved
    """
    def wrapper(file_name, html):
        """
        The wrapper function that handles the html header
        
        :param file_name: the htm file name
        :type file_name: string
        :param html: the html raw text as a list of strings with each line being
            a string item in the list
        :type html: list of str
        
        :returns: resource about the html that will be useful during string 
            matching process
        :rtype: dict
        """
        try:
            # Get the header
            source_url = html[0]
            should_match = html[1]
            # Get the raw html strings
            html_content = html[2:]
            # Striping out empty lines in raw html
            html_content = [ line.strip() if len(line.strip()) else '' for line in html_content ]
        except IndexError as e:
            print "Error accesing html page string: %s" % e
            
        res = {'source_url': source_url,
               'file_name': file_name,
               'should_match': should_match,
               'html_content': html_content,
               'stripped_content': func(file_name, html_content)
               }
        return res
    return wrapper
    
    
def remove_leading_url(func):
    """
    DEPRECATED PLEASE IGNORE!
    
    A decorator that removes the leading url on each html line
    """
    def wrapper(html_fd):
        # Define a partial function that encodes the regex we need to filter out leading urls
        p_filter_func = functools.partial(re.sub, "\s*\[.+\]\s*-\s*", "")
        # Go through the file descriptor and apply the partial filter function to each line
        html_fd_list = map(p_filter_func, html_fd)
        # Pass the modified file descriptor to func
        return func(html_fd_list)
    return wrapper

