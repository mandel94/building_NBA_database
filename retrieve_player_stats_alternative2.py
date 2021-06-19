# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 12:04:56 2021

@author: Manu
"""

# DATA ANALYSIS
import pandas as pd

# WEB-SCRAPING
import bs4

# OTHER PYTHON BUILT-INS
import functools
import re

# CUSTOM MODULES
import scrapy





# =============================================================================
# UTILITIES
# =============================================================================

def extract_stats_names(stats):
    """"""   
    
    names = [s.get("data-stat") \
             for s in stats \
             if isinstance(s, bs4.Tag)]     
    return names
      
              
def extract_stats_list(stats):
    """"""
    
    list_ = [s.string \
             for s in stats \
             if isinstance(s, bs4.Tag)]
    return list_
                
              
def create_stats_dict(stats):
    """For each list of tags (each tag representing one game),
    it returns a dictionary having the stats as keys."""
    
    names = extract_stats_names(stats)
    stats_list = extract_stats_list(stats)
    return {k: stats_list[i] \
            for i, k in enumerate(names)}


def _retrieve_dictionary_stats(player_soups, player_names):
    """"""
     
    _root_url = "https://www.basketball-reference.com"
    stats_links = {}
    for i, p_soup in enumerate(player_soups):
        season_a_tags = [th.a 
                         for table in p_soup.find("table", id="per_game")
                         if isinstance(table, bs4.Tag)
                         for th in table.find_all("th", attrs={"data-stat": "season"})]
        hrefs = [a.get("href") for a in season_a_tags if a is not None]  
        create_link = lambda href: \
                      scrapy.concatenate_href(_root_url, href, False)                        
        stats_links[player_names[i]] = list(set(map(create_link, hrefs)))
                      
        
    stats_soups = {k: [scrapy.create_soup_from_url(v) for v in stats_links[k]]
                    for k in player_names}
    
    # Create table with id for regular season and playoffs.
    # This keys will be used for soup-searching the tables contaning the stats for 
    # the regular season and/or the playoffs.
    table_id_dict = {
            "regular": "pgl_basic",
            "playoffs": "pgl_basic_playoffs"}
        
    # Now we create, for each player, a dictionary containing two other dictionaries,
    # one with the soup object of the stats of regular season, the other with
    # the soup object for the stats of playoffs.  
    table_soups_dict = {k: {} for k in player_names}
    for k in table_soups_dict.keys(): # for each player
        for (season_time, season_time_id) in table_id_dict.items():
            if season_time == "regular":
                stats_tables = [soup.find_all("table", id=season_time_id) \
                                for soup in stats_soups[k]] # == for each season.
                # append dictionary for regular season
                table_soups_dict[k][season_time] = stats_tables
            # For playoffs stats, we need to extract stats from Comment elements. 
            if season_time == "playoffs": 
                is_comment = lambda text: isinstance(text, bs4.Comment)
                find_comments = lambda s: s.find_all(string=is_comment)
                comments_list = list(map(find_comments, stats_soups[k]))
                detect_playoffs_id = lambda comment: \
                                    'id="pgl_basic_playoffs"' in comment.string
                tag_from_comment = lambda comment: bs4.BeautifulSoup(comment, "html.parser")     
                stats_tables = []
                for i, comments in enumerate(comments_list):
                    for comment in comments:
                         if detect_playoffs_id(comment):
                            stats_tables.append(tag_from_comment(comment))
                            break
                # append dictionary for regular season        
                table_soups_dict[k][season_time] = stats_tables
    
    # For each season time (regular and playoffs), 
    #   for each player, 
    #       extract the soup with the stats for that season time, one soup per game,
    #       for each game soup, 
    #       if the player is active,
    #       extract a list with the stats names. Those stats will be used as 
    #       header for the final tables. We are assuming that the set of stats names for 
    #       active players is the most comprehesive one.
    for i, p in enumerate(player_soups):
        if scrapy.is_player_active(p):
            p_name = player_names[i]
            sample_season = table_soups_dict[p_name]["regular"][0][0]
            # [0][0] for 'escaping' ResultSet object
            stats_container = sample_season.find_all("th", attrs={"data-stat": True,
                                                                  "aria-label":True})
            
            stats_names = []
            for stat in stats_container:
                if stat.get("data-stat") not in stats_names:
                    stats_names.append(stat.get("data-stat"))
            break
    
    # Next, let's create a dictionary with players as keys. We will name it 
    # 'players_stats_dict', and it will finally contain the stats of each player.
    # Let's initialize this dictinary, and fill it with soup objects. Later, we 
    # will convert those soup objects in actual tabular form.
    player_stats_dict_v0 = {k: {} for k in player_names}
    for i, p_name in enumerate(player_names):
        player_stats_dict_v0[p_name] = {}
        for season_time in ("regular", "playoffs"):        
            season_time_soups = [sub_el 
                                 for el in table_soups_dict[p_name][season_time]
                                 for sub_el in el] 
            season_time_soups = [s
                                  for s in season_time_soups 
                                  if isinstance(s, bs4.Tag)]
            # Create a function for searching stats.
            stats_search = lambda soup: \
                          soup.find_all("tr", id=re.compile(table_id_dict[season_time]))
            stats = [stats_search(soup) for soup in season_time_soups]
            player_stats_dict_v0[p_name][season_time] = stats
            
 
    # Extract NavigatingStrings for each player, for each game of the year.
    # For each player:
    # - For each season_time (regular and playoffs):
    #   - Take all the season_times that player has played
    #       - For each game in a particular instance of season_time:
    #           - Extract the stats for that game as a string.
    player_stats_dict_v1 = {k: {} for k in player_names}
    for p_name in player_names:
        for season_time in player_stats_dict_v0[p_name].keys():
            player_stats_dict_v1[p_name][season_time] = []
            for season in player_stats_dict_v0[p_name][season_time]:
                for i, game in enumerate(season):
                    game_stats = game.find_all(attrs={"data-stat": True})
                    game_stats = create_stats_dict(game_stats)
                    player_stats_dict_v1[p_name][season_time].append(game_stats)
    
    # Create a third version of 'player_stats_dict', in which stats are extracted
    # from the most comprehensive stats list and pre-allocated with None values.
    # For each player, stats values will be filled with values other than 
    # Nones only if a particular player has those stats recorded.
    player_stats_dict_v2 = {k: {} for k in player_names}
    for p_name in player_names:
        for season_time in ("regular", "playoffs"):
            foo_list = [{k: None for k in stats_names} \
                              for game in player_stats_dict_v1[p_name][season_time]]
            for i, game in enumerate(player_stats_dict_v1[p_name][season_time]):
                foo_list[i].update(game)
            player_stats_dict_v2[p_name][season_time] = foo_list
            
    for p_name, stats in player_stats_dict_v2.items():
        # player_stats_list --> it contains stats (in dictionary format) for  
        # each game the player has played in its career. 
        player_stats_list = [d \
                            for season_time in stats.keys() \
                            for d in stats[season_time]]
        player_stats_dict_v2[p_name] = player_stats_list
    
    return player_stats_dict_v2
               
    
def _get_tabular_stats(player_stats_dict_v2_, player_names_, stats_names_):
    """Convert tabular stats for each player"""
    
    
    # First of all, for each player, let's reduce the list of dictionaries 
    # to a single dictionary containing all values for each stat, appended.
    

       
    def append_dict(d1, d2):
        for stat in stats_names_:
            d1[stat].append(d2[stat])
        return d1

    def reduce(function, iterable, initializer=None):
        it = iter(iterable)
        if initializer is None:
            value = next(it)
        else:
            value = initializer
        for element in it:
            print(element)
            value = append_dict(value, element)
        return value    
        
    initial_dict = {stat: [] for stat in stats_names_}  
    reduce_stats_dict = {}
    tabular_stats_dict = {}
    for p_name in player_names_:
        reduced_dict = reduce(append_dict, 
                              player_stats_dict_v2_[p_name], 
                              initial_dict)
        reduce_stats_dict[p_name] = reduced_dict
        tabular_data = pd.DataFrame(reduce_stats_dict[p_name],
                                    columns=stats_names_)
        tabular_data.set_index("date_game", inplace=True)
        tabular_stats_dict[p_name] = tabular_data
        
    return tabular_stats_dict
    

    ans_1 = _retrieve_dictionary_stats(player_soups, player_names)
    
    for p_name in ans_1.keys():
        for game in ans_1[p_name]:
        
         
         for p_name in player_names_:
            
            unlisted_stats = [[stat \
                               for listed_stat in game_stats \
                               for stat in listed_stat] \
                               for game_stats in season_stats]
            players_stats[player] = pd.DataFrame(unlisted_stats, 
                                                 columns=stats_names_)
            
            players_stats[player].drop("\xa0", axis=1, inplace=True)
        
        # Separate win_loss from final points difference, and put the two into 
        # different columns.
        for k in players_stats.keys():
            to_separate_idx = players_stats[k].columns.get_loc("Win_Loss")
            players_stats[k] = separate_data(players_stats[k], 
                         index=to_separate_idx, 
                         sep="(", 
                         columns=["Win_Loss", "Net_Diff"])
        # Assign current iteration's stats to current iteration's season time.
        table_dict[season_time] = players_stats
        
        
    # CREATE DATAFRAMES FOR THE WHOLE SEASON.    
def _concatenate_season_times(player_name):
  """Concatenate stats for regular season and playoffs."""
  
  regular_found = False
  playoffs_found = False
  
  if player_name in table_dict["regular"].keys():
      regular = table_dict["regular"][player_name]
      regular_found = True
    
  if player_name in table_dict["playoffs"].keys():
      playoffs = table_dict["playoffs"][player_name]
      playoffs_found = True
           
  if regular_found and playoffs_found:
      return pd.concat([regular, playoffs])
  else: 
      if regular_found:
          return regular
      else:
          return playoffs  
  
    # Initialized a final dictionary containing all the stats of each player for 
    # the selected times of season. 
    stats_dict = {k: [] for k in player_name}  
    for p in player_name:
        if time_of_season == "both":
            stats_dict[p] = concatenate_season_times(p) 
        else:
            if p not in table_dict[time_of_season].keys():
                continue
            stats_dict[p] = table_dict[time_of_season][p]
            
    return stats_dict