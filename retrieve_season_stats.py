# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 16:58:14 2021

@author: Manu
"""

# Built-ins
import re

# Web-scraping
from bs4 import BeautifulSoup
import requests



# Custom libraries
from scrapy import map_find


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
# _stat_names = list(map(lambda s: s.lower(), _stat_names))
# _stat_names[0] = "season"
# _stat_names = list(map(lambda s: s.replace(" ", "_"), _stat_names))
      

# Create dictionary for stats_names 
stats_dict = {k: [] for k in _stat_names}     

# Find a way for retrieving stats by iterating over the dictionary keys. The same
# approach followed with player stats. 
         
# Retrieve actual stats.
_stats_containers = map_find(_table_rows, tag=["th", "td"], attr="data-stat")
_get_row_stat = lambda row: [t.a.string for t in row if t.a is not None]
[t.a.string for t in _stats_containers[5]
_row_stats = list(map(_get_row_stat, _stats_containers))


