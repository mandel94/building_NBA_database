#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 14:58:03 2021

@author: mandel94
"""

'''This module will export a connection to MySQL server.
   This connection will function as an interface for building our database  
'''


import os
from getpass import getpass
from mysql.connector import connect, Error


def establish_connection(host_name, user_name, psswd):
    ''''''  
    try:
        with connect(
            host=host_name,
            user=user_name,
            password=psswd,
        ) as connection:
            print('Connection to MySQL Server established!')
            return connection
    except Error as e:
        print("A connection to MySQL Server could not be established")
        return e 


