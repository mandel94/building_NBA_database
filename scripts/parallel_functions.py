# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 15:30:38 2021

@author: Manu
"""

"""Target functions to be applied in parallel. This file is necessary for a pro-
per implementation of the python's multiprocessig modules, that requires target 
functions to be imported from a module different from __main__."""

from scripts.create_player_table.create_player_table import create_player_table


def create_player_table_parallel(inf_, sup_, manager_list):
    return_list = []
    try:
        return_list.append(create_player_table(inf=inf_, sup=sup_))
    except Exception as e:
        return_list.append(None)
    manager_list.append(return_list)
    
    