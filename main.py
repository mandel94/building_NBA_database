# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:08:11 2021

@author: Manu
"""

# DATA ANALYSIS
import pandas as pd
import numpy as np


# PROFILING
import time


# IMPORT CUSTOMS.
from retrieve_player_stats_alternative2 import retrieve_player_stats
import scrapy
from create_player_table import create_player_table
from retrieve_season_stats import retrieve_season_stats

# Create player table.
# Player table will be separated into slices of 100 + residual to the total num-
# ber of players. 
# Total number of players is 4897.
# Choose the number of players to retrieve the stats for. 
_nb_of_players = 200
# Number of slices 
_slices = 2
_step = _nb_of_players // _slices
_inf = 0
_player_table_slices = [] 
_player_soups_slices = []
_player_names_slices = []
_time_profiling = [] 
for i in range(_slices):
    _start = time.time()
    _sup = _inf + (_step - 1)
    if _sup not in range((_nb_of_players - _step), _nb_of_players):
        _players = create_player_table(_inf, _sup)
        _player_table_slices.append(_players[0])
        _player_soups_slices.append(_players[1])
        _player_names_slices.append(_players[2])
        _inf = _sup + 1
    else:
        _residual = _nb_of_players % _step
        _sup = _sup + _residual
        _players = create_player_table(_inf, _sup)
        _player_table_slices.append(_players[0])
        _player_soups_slices.append(_players[1])
        _player_names_slices.append(_players[2])
    _end = time.time()
    _time_profiling.append(_end - _start)
    
    
    
players = create_player_table(inf=0, sup=100)
player_table = players[0]
player_soups = players[1]  
player_names = players[2]  


# Save test file.
player_table.to_csv("test_player_table")

# Retrieve dictionary with players' stats.
stats_dict = retrieve_player_stats(player_soups=player_soups, 
                                   player_names=player_names)
# Retrieve season stats.
season_stats = retrieve_season_stats()
season_stats.to_csv("season_stats.csv")


# Save test file.
stats_dict['Kareem Abdul-Jabbar'].to_csv("abdul_jabbar_career.csv")

# Create grand table with stats for all players. 
grand_stats_table = pd.concat(stats_dict.values())
