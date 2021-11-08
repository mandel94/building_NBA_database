# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 12:55:56 2021

@author: Manu
"""

# Built-in
import re

def separate_column(data, index, sep, columns):
    """ Separate data of the indexed column of data in correspondence of a separator 
    and map-assign splitting results to the provided columns.
    
    
    Args:
        - data --> A dataframe. 
        - index --> An integer, or column name, specifying the column to be splitted.
        - sep --> Splitting point. Supported separator are '_', '-', '.', '(', '[' '{'.
        - columns --> string, or list of strings, specifying the name of the 
                      columns to which the outputs of the splitting operation 
                      will be assigned.
    
    Returns:
        A dataframe containing all the columns of the data argument but the splitted
        column, plus the columns obtained as output from the splitting operation.
    """
    df = data.copy(deep=True)
    if isinstance(index, str):
        index = data.columns.get_loc(index)
    to_separate = df.iloc[:, index]
    df.drop(df.columns[index], axis=1, inplace=True)
    # idx_values = to_separate.index
    if sep in ["(", "[", "{"]:
        if sep == "(":
            mirror_sep = ")"
        elif sep == "[":
            mirror_sep = "]"
        elif sep == "{":
            mirror_sep = "}"
        map_step_1 = list(map(lambda x: re.split("\\" + sep + "|" + "\\" + mirror_sep, x), to_separate))
        map_step_2 = list(map(lambda x: [elem for elem in x if elem != ""], map_step_1))
        col_1 = [elem[0] for elem in map_step_2]
        col_2 = [elem[1] for elem in map_step_2]
        df.insert(loc=index, column=columns[0], value=col_1)
        df.insert(loc=index, column=columns[1], value=col_2)
    else:
        map_step = list(map(lambda x: re.split(sep, x), to_separate))
        col_1 = [elem[0] for elem in map_step]
        col_2 = [elem[1] for elem in map_step]
        df.insert(loc=index, column=columns[0], value=col_1)
        df.insert(loc=index, column=columns[1], value=col_2)
    return df



class DataCleaner():
    """Data cleaner with a functional approach.
    The idea is to create a class for applying previously defined functions to
    each element of an input. The input can be an iterable object, a 
    dictionary or a dataframe."""
    
    def __init__(self, obj):
        """"""   
        self.input = obj
        
    def apply(self, function, **kwargs):
        """Apply a function to each element of the object given as input."""
        if isinstance(self.input, dict):
            for k in self.input.keys():
                if len(kwargs) > 1:
                    self.input[k] = function(self.input[k], kwargs)
                else:
                    self.input[k] = function(self.input[k])
        elif isinstance(self.input, list):
            for i in range(len(self.input)):
                self.input[i] = function(self.input[i])
        else:
            self.input = function(self.input)
                
        return self
    
                


      
                
            
          
