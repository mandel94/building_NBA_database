# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:08:11 2021

@author: Manu
"""

# STANDARD
import sys

# DATA ANALYSIS
import pandas as pd
import numpy as np

# PARALLEL PROCESSING TOOLKIT
from multiprocessing import cpu_count, Process
import parallel_functions

# PROFILING
import time

# DEBUGGING
import pdb


# IMPORT CUSTOMS.
from retrieve_player_stats_alternative2 import retrieve_player_stats
from create_player_table import args_create_player_table, create_player_table
from retrieve_season_stats import retrieve_season_stats
from data_persistence import pickle_save
from parallel_processing_toolkit import Multiprocessor
from parallel_functions import create_player_table_parallel
from list_functions import chunks


# CREATE PLAYER TABLE.
# Prepare big list with arguments to create player_table, to be splitted into parallel processes. 
big_args = args_create_player_table(nb_of_players=50, step=10)


# Prepare multiprocessing interface.
mp = Multiprocessor(nb_cores=cpu_count())
for i, args in enumerate(big_args):
    big_args[i] = args + (mp.results, )
    
mp.define_parallel_task(parallel_functions.create_player_table_parallel, big_args)

# Apply parallel computation.
start = time.time()
processes = []

if __name__ == "__main__":
    for p in mp.processes:
        p.start()
        print("Process " + p.name + " has started")
    for p in mp.processes:
        p.join()
end = time.time()
time_profiling = end - start

 

# import copy
# to_reduce = copy.deepcopy(_player_table_slices)
# reduced_player_table = pd.concat(to_reduce, axis=0)
# reduced_player_table.to_csv("grand_player_table_slice.csv")
    
    
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
