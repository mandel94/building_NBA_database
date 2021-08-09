# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:08:11 2021

@author: Manu
"""

<<<<<<< HEAD
# STANDARD
=======
# STANDARDf
>>>>>>> implement_parallel_processing


# DATA ANALYSIS
import pandas as pd
import numpy as np

# PARALLEL PROCESSING TOOLKIT
from multiprocessing import cpu_count, Process
import parallel_functions

# PROFILING
import time
from profiling import TimeProfiler

<<<<<<< HEAD
# DEBUGGING
import pdb
=======
>>>>>>> implement_parallel_processing


# IMPORT CUSTOMS.
from retrieve_player_stats_alternative2 import retrieve_player_stats
from create_player_table import args_create_player_table, create_player_table
from retrieve_season_stats import retrieve_season_stats
from data_persistence import pickle_save
from parallel_processing_toolkit import Multiprocessor
from parallel_functions import create_player_table_parallel
from list_functions import chunks


<<<<<<< HEAD
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


=======


# Create table of players stats, from the first player [0+1th] to the last 
# players [4897th]
players = create_player_table(0, 4897)

>>>>>>> implement_parallel_processing
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
