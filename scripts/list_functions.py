# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 16:27:54 2021

@author: Manu
"""

"""This module contains all functions involving lists."""

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]