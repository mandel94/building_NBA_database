# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:08:11 2021

@author: Manu
"""
from retrieve_player_stats_alternative2 import retrieve_player_stats
import scrapy
from create_player_table import create_player_table

# TESTING PURPOSES 
# t = ["Boston Celtics", "Chicago Bulls"] # team
# t_s = "2012-13"  # team season
# p = "all" # players
# p_s = "2012-13"  # players season
# tm_s = "both" # time_of_season ["regular" | "playoffs" | "both"]


# stats_dict = retrieve_alt(team=t, 
#                           team_season=t_s, 
#                           players=p, 
#                           players_season=p_s,
#                           time_of_season=tm_s)



players = create_player_table()
player_table = players[0]
player_soups = players[1]  
player_names = players[2]  
player_links = players[3]


stats_dict_alt = retrieve_player_stats(player_soups, player_names)
    