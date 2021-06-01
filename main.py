# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:08:11 2021

@author: Manu
"""
from retrieve_stats import retrieve_NBA_stats

t = "all" # team
t_s = "2010-11"  # team season
p = "all" # players
p_s = "2010-11"  # players season
tm_s = "both" # time_of_season ["regular" | "playoffs" | "both"]


test = retrieve_NBA_stats(team=t, 
                          team_season=t_s, 
                          players=p, 
                          players_season=p_s,
                          time_of_season=tm_s)



