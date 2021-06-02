# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 19:46:29 2021

@author: Manu
"""


# =============================================================================
# UTILITIES 
# =============================================================================

def change_stats_name(df, names, in_place):
    """"""
    rename_dict = {k: names[i] for i, k in enumerate(df.columns)}
    df.rename(columns=rename_dict, inplace=in_place)
    return(df)


def reformat_age(age):
    """This function reformats the age value as it is originally presented in
       the 'basketball-reference' tables.
       
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
    
       
def reformat_age_list(df):
    """Apply reformat_age function to each element of a list."""
    
    age_list = list(df.loc[:, "age"])
    new_age_list = list(map(reformat_age, age_list))
    df["age"] = new_age_list
    
                                    
    
stats_names = ["rank", "season_game", "age", "team", "opponent", "net_diff", 
               "win_loss", "games_started", "minutes_played", 
               "field_goals", "field_goal_attempts", "field_goal_percentage",
               "3_point_field_goals", "3_point_field_goal_attempts",
               "3_point_field_goal_percentage", "free_throws", "free_throw_attempts", 
               "free_throw_percentage", "offensive_rebounds", "defensive_rebounds",
               "total_rebounds", "assists", "steals", "blocks", "turnovers", 
               "personal_fouls", "points", "game_score", "plus_minus"]





# =============================================================================
# MAIN FUNCTION 
# =============================================================================

def prepare_data(stats_dict):
    """This function prepares the data for storage in the database."""
    
    for team in stats_dict.keys():
        for player in stats_dict[team]:
            change_stats_name(stats_dict[team][player], stats_names, in_place=True)
            reformat_age_list(stats_dict[team][player])
        
    return stats_dict
        
        
