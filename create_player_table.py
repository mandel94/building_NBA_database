# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:47:13 2021

@author: Manu
"""

import pandas as pd
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
    _create_link = lambda href: scrapy.concatenate_href(_root_url, href, remove_last_dir=True)
    _player_links = list(map(_create_link, _player_hrefs))[0:19]
    _soups = create_soups_from_hrefs(_player_hrefs[0:19])
    _soups_to_export = _soups
    
    # Collect players' informations.
    _name = [tag.span.string
              for soup in _soups
              for tag in soup.find_all("h1", attrs={"itemprop": "name"})]
    
    _position = [tag.next_sibling
                 for soup in _soups
                 for tag in soup.find_all("strong", text=re.compile(" Position:"))]  
    _pos_search = lambda x: re.search("[a-z]+(\\s[a-z]+)*", x, re.IGNORECASE)
    _position = [_pos_search(pos).group(0) for pos in _position]
    
    _shoots = [tag.next_sibling
               for soup in _soups
               for tag in soup.find_all("strong", text=re.compile(" Shoots:"))]  
    _shoots_search = lambda x: re.search("[a-z]+(\\s[a-z]+)*", x, re.IGNORECASE)
    _shoots = [_shoots_search(s).group(0) for s in _shoots]
    
    _height_and_weight = [tag.next_sibling
                          for soup in _soups
                          for tag in soup.find_all("span", attrs={"itemprop": "weight"})]
    _height_search = lambda x: re.search("([0-9]+)cm", x)
    _height = [_height_search(el).group(1) for el in _height_and_weight]
    
    _weight_search = lambda x: re.search("([0-9]+)kg", x)
    _weight = [_weight_search(el).group(1) for el in _height_and_weight]
        
    
    def _soup_search(soup):
        """It returns a different search depending on whether the player is 
           still active or not."""
        
        if scrapy.is_player_active(soup):
            _search = soup.find_all("strong", text=re.compile("Experience:"))
            return _search
        else:
            _search = soup.find_all("strong", text=re.compile("Career Length:"))
            return _search
        
           
    _experience = [tag.next_sibling
                   for soup in _soups
                   for tag in _soup_search(soup)]
    
    
    _experience = [el.split()[0] for el in _experience]
    
    def _assign_null_to_rookie(x):
        """Assign null values to rookies' experience."""
        
        if re.match("rookie", x, re.IGNORECASE):
            return "0"
        else:
            return x
        
    _experience = list(map(_assign_null_to_rookie, _experience))
    
    _country = [tag
                for soup in _soups
                for tag in soup.find_all("span", attrs={"itemprop": "birthPlace"})]
    
    def extract_country_name(tag):
        """"""
        if tag.a is None:
            return None
        else:
            return tag.a.string
        
    _country = list(map(extract_country_name, _country))
        
    
    # Create Dataframe
    _columns = [_name, _position, _height, _weight, _shoots, _experience, _country]    
    _column_names = ["name", "position", "height", "weight", "shoots", "experience", 
                     "country"]
    player_table = pd.DataFrame(data={k: _columns[i] for i, k in enumerate(_column_names)})
    
    return (player_table, _soups_to_export, _name, _player_links)
     
    
