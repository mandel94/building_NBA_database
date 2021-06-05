# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:08:11 2021

@author: Manu
"""
from retrieve_stats import retrieve_player_stats
import scrapy

t = ["Boston Celtics", "Chicago Bulls"] # team
t_s = "2012-13"  # team season
p = "all" # players
p_s = "2012-13"  # players season
tm_s = "both" # time_of_season ["regular" | "playoffs" | "both"]



stats_dict = retrieve_player_stats(team=t, 
                          team_season=t_s, 
                          players=p, 
                          players_season=p_s,
                          time_of_season=tm_s)

players = create_player_table()
    

print(players.to_string())
