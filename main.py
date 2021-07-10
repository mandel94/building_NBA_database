# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:08:11 2021

@author: Manu
"""

# DATA ANALYSIS
import pandas as pd
import numpy as np

# PARALLEL PROCESSING TOOLKIT
from multiprocessing import cpu_count

# PROFILING
import time


# IMPORT CUSTOMS.
from retrieve_player_stats_alternative2 import retrieve_player_stats
from create_player_table import args_create_player_table, create_player_table
from retrieve_season_stats import retrieve_season_stats
from data_persistence import pickle_save
from parallel_processing_toolkit import Multiprocessor
from parallel_functions import create_player_table_parallel
from list_functions import chunks


# CREATE PLAYER TABLE.
# Prepare big list with arguments to be splitted into parallel processes. 
big_args = args_create_player_table(nb_of_players=1000, step=100)

# Prepare multiprocessing interface.
mp = Multiprocessor(nb_cores=cpu_count())
mp.define_parallel_processes(target=create_player_table_parallel, args=big_args)

# Apply parallel computation.
start = time.time()
if __name__ == "__main__":
    for p in mp.processes:
        p.start()
        print("{} started".format(p.name))
    for p in mp.processes:
        p.join()
end = time.time()
time_profiling = end - start

 
for i in range(_slices):
    start = time.time()
    end = time.time()
    time_profiling.append(_end - _start)

# import copy
# to_reduce = copy.deepcopy(_player_table_slices)
# reduced_player_table = pd.concat(to_reduce, axis=0)
# reduced_player_table.to_csv("grand_player_table_slice.csv")
    
    
players = [sub_el for el in _player_names_slices for sub_el in el]
    
# players = create_player_table(inf=0, sup=100)
# player_table = players[0]
# player_soups = players[1]  
# player_names = players[2]  


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
