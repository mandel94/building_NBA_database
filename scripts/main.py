# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:08:11 2021

@author: Manu
"""

# STANDARDf


# DATA ANALYSIS
import pandas as pd
import numpy as np

# PARALLEL PROCESSING TOOLKIT
from multiprocessing import cpu_count, Process
import parallel_functions

# PROFILING
import time
from profiling import TimeProfiler



# IMPORT CUSTOMS.
from retrieve_player_stats_alternative2 import retrieve_player_stats
from create_player_table import args_create_player_table, create_player_table
from retrieve_season_stats import retrieve_season_stats
from data_persistence import pickle_save
from parallel_processing_toolkit import Multiprocessor
from parallel_functions import create_player_table_parallel
from list_functions import chunks




# Create table of players stats, from the first player [0+1th] to the last 
# players [4897th]
players = create_player_table(0, 4897)

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
