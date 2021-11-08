# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 16:10:32 2021

@author: Manu

"""

# PROFILING
import time

class TimeProfiler():
    """An interface for time profiling snippets of code.
    
    Each snippets of code must be passed through a function object that runs
    that code when called."""
    
    def __init__(self, function):
        """Args:
            - function --> the function executing the code to be profiled."""
        self.function = function
        
    def time_profile(self):
        """Basic time profiling of `self.function`.
        
        Returns --> seconds that running `self.function` has taken."""
        start = time.time()
        self.function()
        end = time.time()
        return (end - start)