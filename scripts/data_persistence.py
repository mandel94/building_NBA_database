# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 20:41:42 2021

@author: Manu
"""

import pickle

def pickle_save(obj, path):
    """"""
    with open(path, "wb") as file:
        pickle.dump(obj, file)
    