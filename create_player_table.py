# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:47:13 2021

@author: Manu
"""

from bs4 import BeautifulSoup
import requests
import re

import scrapy




# =============================================================================
# UTILITIES
# =============================================================================

def check_parents_attribute(tag, attrs):
    """This function checks if the tag has at least one parent respecting the 
       key-value pair defined in attrs, where the key is a valid CSS attribute.   
    """
    _parents = tag.parents
    attr = [attr for attr in attrs.keys()][0]
    attr_value = attrs[attr]
    #####################
    for p in _parents:
        if p.get(attr) is None:
            continue
        else:
            tag_attrs = p.get(attr)
        if attr_value in tag_attrs:
            return True
    #####################
    return False


def concat_mapping_fun(href):
        """"""
        return scrapy.concatenate_href(_root_url, 
                                       href, 
                                       remove_last_dir=True)
    
def create_soups_from_hrefs(hrefs_list):
    """"""
    _links = list(map(concat_mapping_fun, hrefs_list))
    _reqs = list(map(requests.get, _links))
    _soups = list(map(lambda req: BeautifulSoup(req.content, "html.parser"), _reqs))
    return _soups
    
        
        
            


# =============================================================================
# DEFINITIONS
# =============================================================================

_root_url = "https://www.basketball-reference.com/players/"
_req = requests.get(_root_url)
_soup_root = BeautifulSoup(_req.content, "html.parser")





# =============================================================================
# MAIN FUNCTION
# =============================================================================
def create_player_table():
    """This function creates a descriptive table for all NBA players."""
    
    # Create the link for letters indexes (for accessing the page if players 
    # whose name starts with a certain letter)
    _index_tags = [tag.a
                  for tag in _soup_root.find_all("li") 
                  if check_parents_attribute(tag, attrs={"class": "page_index"})]
    _index_hrefs = [tag.get("href") for tag in _index_tags if tag is not None]
    _soups = create_soups_from_hrefs(_index_hrefs)
    
    # Create links for accessing each player's stats.
    _player_hrefs = [th.a.get("href")
                     for soup in _soups
                     for th in soup.find_all("th", attrs={"data-stat": "player"})
                     if th.a is not None]
    _soups = create_soups_from_hrefs(_player_hrefs[0:9])
    
    # Collect players' informations.
    _name = [tag.span.string
              for soup in _soups
              for tag in soup.find_all("h1", attrs={"itemprop": "name"})]
    
    _position = [tag.next_sibling
                 for soup in _soups
                 for tag in soup.find_all("strong", text=re.compile(" Position:"))]  
    _pos_search = lambda x: re.search("[a-z]+(\\s[a-z]+){0,4}", x, re.IGNORECASE)
    _position = [_pos_search(pos).group(0) for pos in _position]
