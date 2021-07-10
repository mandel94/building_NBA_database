# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 15:30:38 2021

@author: Manu
"""

"""Target functions to be applied in parallel. This file is necessary for a pro-
per implementation of the python's multiprocessig modules, that requires target 
functions to be imported from a module different from __main__."""

from create_player_table import create_player_table
from parallel_processing_toolkit import Multiprocessor


def create_player_table_parallel(args_list):
    return_list = []
    errors = []
    error_args = []
    for args in args_list:
        try:
            return_list.append(create_player_table(inf=args[0], sup=args[1]))
            errors.append(None)
            error_args.append(None)
        except Exception as e:
            return_list.append(None)
            errors.append(e)
            error_args.append(args)
    return_dict = {
        "player_tables": return_list,
        "errors": errors,
        "error_args": error_args}
    return return_dict