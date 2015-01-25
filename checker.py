#!/usr/bin/env python

__version__ = 0.1

from config import Config
from factories import Data_Factory, Page_Factory
from strategy import Strategy, mass_page_match, baseline_match, magic_speedy_match


def main():
    # Display the config
    Config.show_config()
    
    # Create our data and page factories
    data_factory = Data_Factory()
    page_factory = Page_Factory()
    
#     # Dump data to files for debug purpose
#     data_factory.dump_to_disk('data_processed')
#     page_factory.dump_to_disk('stripped_html')
     
    # Now we can use different strategies to find matches    
    #baseline_strategy = Strategy(baseline_match)
    #baseline_strategy.find_match(data_factory, page_factory)
    
    #mass_page_match_strategy = Strategy(mass_page_match)
    #mass_page_match_strategy.find_match(data_factory, page_factory)
    
    # Now we can use different strategies to find matches    
    baseline_strategy = Strategy(magic_speedy_match)
    baseline_strategy.find_match(data_factory, page_factory)

if __name__ == '__main__':
    main()
