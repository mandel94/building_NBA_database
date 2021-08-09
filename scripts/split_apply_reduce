#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 16:40:16 2021

@author: mandel94
"""

# CREATE PLAYER TABLE (Total number of players: 4897)
# Prepare big list with arguments to create player_table, to be splitted into parallel processes.
# Split! 
big_args = args_create_player_table(nb_of_players=4897, step=1000)

# Apply!
player_table_list = []
player_soup_list = []
player_name_list = []
for args in big_args:
    players = create_player_table(args[0], args[1])
    player_table_list.append(players[0])
    player_soup_list.append(players[1])
    player_name_list.append(players[2])
    print("Slice completed!")
    

    
t = TimeProfiler(with_split_profile)
time_with_split = t.time_profile()

t = TimeProfiler(without_split_profile)
time_without_split = t.time_profile()
    
# Reduce!