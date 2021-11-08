# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:08:11 2021

@author: Manu
"""



# DATA ANALYSIS
import pandas as pd

# IMPORT CUSTOMS
from scripts.retrieve_player_stats.retrieve_player_stats_alternative2 \
    import retrieve_player_stats
from scripts.create_player_table.create_player_table import create_player_table
from scripts.create_season_table.retrieve_season_stats import retrieve_season_stats
from scripts.utils.prepare_stats_data import prepare_data



# CREATE PLAYER TABLE (Total number of players: 4897)
# Create table of players stats, from the first player [0+1th] to the last 
# players [4897th]
players = create_player_table(0, 10)


# Retrieve dictionary with players' stats.
stats_dict = retrieve_player_stats(player_soups=players[1], 
                                   player_names=players[2])


# Apply transformations defined in 'prepare_stats_data.py' file
prepare_data(stats_dict)


# Retrieve season stats.
season_stats = retrieve_season_stats()
# season_stats.to_csv("season_stats.csv")


# Create grand table with stats for all players. 
grand_stats_table = pd.concat(stats_dict.values())
