#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 12:35:43 2021

@author: mandel94
"""


from create_player_table import create_player_table
import pdb
 
# DEBUG CREATE_PLAYER_TABLE
# There is a problem with height and weight vectors, that are shorter than the 
# other one by one point.


players = create_player_table(2500, 2550)

# Find out index of error 
for i, p in enumerate(players):
    try:
        p[0][1]
    except:
        print(i, p)
        
# Compare res with error against res without error...
print(players[42])
print(players[0])

# ... There is an empty element in 'players' list. 
# It come from the player 'Dick Lee' (2542th player). 
# The problem lays on the fact that 'find_all("span", attrs={"itemprop": "weight"})'
# does not find anything at all.


