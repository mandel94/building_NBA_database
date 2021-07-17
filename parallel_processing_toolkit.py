# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 18:49:47 2021

@author: Manu
"""

"""This module provides a toolkit for implementing parallel processing. 
"""

# Multi-processing modules.
from multiprocessing import Process, Queue, Lock, Pool, cpu_count, Manager
import queue 


class Multiprocessor():
    """An interface for applying parallel computing.
    
    Attributes:
        Init:
            - self.nb_cores
            - self.results
        After calling define_parallel_processing method:
            - self.target
            - self.processes
            - self.splits
        
        """
    
    def __init__(self, nb_cores, results=None):
        """Initialize a multiprocessore object
        
        Args:
            -nb_cores: int. The number of cores at the disposal of the CPU. It
            determines the number of processes to be created in a parallel 
            computation task.
            - results: object of class multiprocessing.managers.ListProxy. This
            object is useful for merging the outputs of parallel processes into
            one bucket.
        """
        self.n_processes = nb_cores
        if results is None:
            self.results = Manager().list() 
            
    def split(self, args):
        """Split items of args among detected cores.
            - args: arguments to be splitted"""  
            
        split_step = len(args) // self.n_processes
        splits = []
        for i in range(self.n_processes):
            if i == self.n_processes - 1:
                args_split = args[(i*split_step):]
            else:
                args_split = args[(i*split_step):(i*split_step + split_step)]
            splits.append(args_split)
        self.splits = splits
        return self.splits
        
        
    def define_parallel_task(self, target, args):
        """Define processes to be run on parallel.
        
        This method allows to apply basic pa
        rallel programming. It executes in 
        parallel the same target function to each of element of args.
        
        Args:
            - target --> function object.
            - args --> a python iterable. Each single element should be a tuple
              containing all the arguments required by the target function."""
            
        self.target = target
        processes = [Process(target=self.target, args=a) \
                     for a in args]
        self.processes = processes
            
        
    def define_parallel_batch_task(self, target, args, split_idx="all"):
        """Define the processes to be run in parallel, on a batch of data.
        
        This method can provide great parallelism gains in case we need to apply  
        some instruction stream on a large quantity of data (for example, a very
        long list). It allows to apply the same instruction stream on different
        splits of the data, with each split of data being processed in parallel.
        
        Each process is defined by a target function to be applied to an iterable.
        The iterable is obtained by dividing `args` into equal pieces, to be than 
        assigned to each of the #nb_cores cores. 
        (i.e., the overall task is splitted into sub-tasked to be run in parallel).
        The elements of the iterable are thus the different set of arguments for the 
        target function, which will run in parallel for each element of the iterable, 
        and than merge each sub result into one common list (accessible through
        `self.results`. 
        
        Args:
            - target: function object. 
            - args: whatever object that can be splitted into slices (such as 
                    a tuple or a list).
            - split_idx: int. `args` will be splitted 
        """
        
        self.target = target
        if split_idx == "all":
            split_step = len(args) // self.n_processes
            splits = []
            for i in range(self.n_processes):
                if i == self.n_processes - 1:
                    args_split = args[(i*split_step):]
                else:
                    args_split = args[(i*split_step):(i*split_step + split_step)]
                splits.append(args_split)
            processes = [Process(target=self.target, args=(s,)) \
                         for s in splits]
            self.processes = processes
            self.splits = splits
    
    
        