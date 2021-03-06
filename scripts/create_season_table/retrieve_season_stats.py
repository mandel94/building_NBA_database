# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 16:58:14 2021

@author: Manu
"""

# Built-ins

# Data analysis
import pandas as pd

# Web-scraping
from bs4 import BeautifulSoup
import requests

# Other utilities
from functools import reduce

# Custom libraries
from scripts.utils.scrapy import map_find


# UTILITIES

def _extract_identifier(tag):
    '''Scrape the player's unique identifier'''
    id_ = tag.get('href').split('/').pop().split('.')[0]
    return id_



def _get_row_stat(row):
    '''Retrieve stats from table rows'''
    row_stats = []
    # Initalized a counter for proper statistic extraction
    count = 0
    for tag in row:
        if tag.a is not None:
            if count in [0, 1, 2]:
                row_stats.append(tag.a.string)
            else:
                row_stats.append(_extract_identifier(tag.a))
        else:
            row_stats.append(None)
        count += 1
    return row_stats



def retrieve_season_stats():
    """This function retrieves the main stats for each season in a tabular form."""
    
    # Get access to table containing season stats --> This will be out point of en-
    # try when web-scraping the stats.
    _req = requests.get("https://www.basketball-reference.com/leagues/")
    _root_access_point = BeautifulSoup(_req.content, "html.parser")
    _season_access_point = _root_access_point.find("table", id="stats")
    
    # Retrieve rows of the table containing the stats. 
    _table_rows = _season_access_point.find_all("tr")
                        
    # Define a function for retrieving stats. We will map-apply it to each row of 
    # the table.
    
    # First, let's retrieve stats names.
    _stat_names = _table_rows[1].find_all(attrs={"aria-label":True})
    _stat_names = [tag.get("aria-label") for tag in _stat_names]
    _stat_names = list(map(lambda s: s.lower(), _stat_names))
    _stat_names[0] = "season"
    _stat_names = list(map(lambda s: s.replace(" ", "_"), _stat_names))
               
    # Retrieve actual stats.
    _stats_containers = map_find(_table_rows, tag=["th", "td"], attr="data-stat")
    # First two rows do not include stats. 
    _stats_containers = _stats_containers[2:]
     
    _row_stats = list(map(_get_row_stat, _stats_containers))
    
    _season_stats_list = []
    # For each season:
        # create dictionary with stats;
        # append it to overall _season_stats_list. 
    for season_stats in _row_stats:
        # Initialize list of dictionaries, where each dictionary contains the 
        # stats for one season.
        _stats_dict = {k:[] for k in _stat_names}
        for i, k in enumerate(_stats_dict.keys()):
            _stats_dict[k] = season_stats[i]
        _season_stats_list.append(_stats_dict)
        
    
    # Let's reduce the single dictionaries into a grand dictionary.
    
    def _append_dict(d1, d2):
        for stat in _stat_names:
            d1[stat].append(d2[stat])
        return d1
            
    _reduce_stats_dict = {} 
    _initial_dict = {stat: [] for stat in _stat_names}
    _reduced_stats_dict = reduce(_append_dict, _season_stats_list, _initial_dict)
    
    # Convert the grand dictionary into a pandas dataframe.
    _season_stats = pd.DataFrame(_reduced_stats_dict, columns=_stat_names)   
    return _season_stats
     
