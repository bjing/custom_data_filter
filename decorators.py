import functools
import re
import os
import copy

"""
Decorators for HTML parsing
"""

def handle_html_header(func):
    """
    A decorator that handles our special kind of html file, whcih has first two lines reserved
    """
    def wrapper(file_name, html):
        """
        """
        # Get the header
        source_url = html[0]
        should_match = html[1]
        # Duplicate the file descriptor to return a list of all html raw content
        html_content = html[2:]
        html_content = [ line.strip() if len(line.strip()) else '' for line in html_content ]
        
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

def normalise(func):
    """
    A decorator that removes the leading url on each html line
    """
    def wrapper(html_fd):
        return func(html_fd)
    return wrapper

"""
Decorators for term matching
"""

def ignore_exclusions(func):
    """
    TODO We shouldn't match any terms that are on exclusion list
    """
    @functools.wraps
    def wrapper(html_fd):
        return func()
    return wrapper
