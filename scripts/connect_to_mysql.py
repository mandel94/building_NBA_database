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
from mysql.connector import connect, Error, errorcode




class DBConnection():
    '''A class for working properly with connections to the database.
       It is suited for context managers, allowing proper "cleaning up"
       after database operations are completed
    '''
    def __init__(self):
        self.host_name = 'localhost'
        self.user_name = os.environ.get("MYSQLUSER")
        self.psswd = os.environ.get("MYSQLPSSWD")

    def __enter__(self):
        try:
            cnx = connect(
                host=self.host_name,
                user=self.user_name,
                password=self.psswd)       
            print('Connection to MySQL Server established!')
            self.connection = cnx
        except Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif e.errno == errorcode.ER_BAD_DV_ERROR:
                print("Database does not exist")
            else:
                print(e)     
        else:
            return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
           
    
        
__all__ = ['DBConnection']

