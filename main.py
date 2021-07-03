# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:08:11 2021

@author: Manu
"""
from retrieve_player_stats_alternative2 import retrieve_player_stats
import scrapy
from create_player_table import create_player_table
from retrieve_season_stats import retrieve_season_stats

# Create player table.
players = create_player_table()
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
season_stats.to_csv("season_stats")


# Save test file.
stats_dict['Kareem Abdul-Jabbar'].to_csv("abdul_jabbar_career.csv")


