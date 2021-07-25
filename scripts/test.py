# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 18:09:11 2021

@author: Manu
"""
players = create_player_table(2500, 2600)
columns = [players[k] for k in players.keys()]
    
list(map(len, columns))

