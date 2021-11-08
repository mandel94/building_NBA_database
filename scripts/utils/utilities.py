# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 11:06:17 2021

@author: Manu
"""

import re

# =============================================================================
# CREATE PLAYER TABLE
# =============================================================================

"""Search Regex

    This function is used for retrieving information on players stats through
    regex matching. If no match is found, None is returned. """

def search_stat(x):
   regex_search = re.search("[a-z]+(\\s[a-z]+)*", x, re.IGNORECASE)
   if regex_search is not None:
       return regex_search.group(0)
   else:
       return None 
   
    


    