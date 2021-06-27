# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 19:46:29 2021

@author: Manu
"""



def change_stats_name(df, names, in_place):
    """"""
    rename_dict = {k: names[i] for i, k in enumerate(df.columns)}
    df.rename(columns=rename_dict, inplace=in_place)
    return(df)


def reformat_age(age):
    """This function reformats the age value.
       
       Transformation:
           #years-#days -> (#years).(fraction of 1 year from last birthday)          
    """
    # Split
    age_splitted = age.split("-")
    # Transform decimal part.
    decimal_part = round(int(age_splitted[1]) / 365, 2) * 100
    decimal_part = str(int(decimal_part)) # 0.74 -> 74 -> '74'
    age_splitted[1] = decimal_part
    # Collapse
    new_age = ".".join(age_splitted)
    return float(new_age)
    
       
def reformat_age_column(df):
    """Apply reformat_age function to each element of the age column."""
    
    age_list = list(df.loc[:, "age"])
    new_age_list = list(map(reformat_age, age_list))
    df["age"] = new_age_list
    return df
    

def reformat_location_column(df):
    """Change location values to 'Home' / 'Away'."""
    
    def replace(loc):
        if loc == "@":
            return "away"
        else:
            return "home"
        
    df['game_location'] = list(map(replace, df['game_location']))
    return df 
    

        
        
