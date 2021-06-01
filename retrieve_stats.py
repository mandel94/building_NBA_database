import requests
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup, Comment
from scrapy import *

# =============================================================================
# UTILITIES
# =============================================================================





# =============================================================================
# MAIN FUNCTION
# =============================================================================
def retrieve_NBA_stats(team="all", 
                       team_season="2020-21", 
                       players="all", 
                       players_season="2020-21", 
                       time_of_season="both"):
    """Retrieve NBA stats.
    
       Statistics are retrieved from www.basketball-reference.com. 
       
       Args:
           - team: string. Toghether with 'team_season', this defines the roster 
                   of which the stats will be retrieved.
           - team_season: string. Toghether with 'team', this defines the roster 
                          of which the stats will be retrieved.
           - players: list of strings, or single string. Players whose stats will 
                      be retrieved. Select 'all' for selecting all players.
           - players_season: list of strings, or single string. The season for 
                             which the stats will be retrieved.
           - time_of_season: string. Retrieve stats for regular season and/or 
                             playoffs. Possible values are:
                                 1. 'Regular'
                                 2. 'Playoffs'
                                 3. 'Both'
                                 
    """
    

    root_url = "https://www.basketball-reference.com/teams/"
    # Create root soup object
    req = requests.get(root_url)
    soup = BeautifulSoup(req.content, "html.parser")
    
    # Search for teams
    if team == "all":
        team_names = [tag.string for tag in \
                         soup.find_all(attrs={"data-stat": "franch_name"})]
        team_names = [name for name in team_names if name != "Franchise"]
        teams_a_tags = [tag.a for tag in \
                         soup.find_all(attrs={"data-stat": "franch_name"})]
        team_hrefs = [tag.get("href") for tag in teams_a_tags \
                        if tag is not None]
    else:
        teams_a_tags = [tag.find("a", text=team) for tag in \
                         soup.find_all(attrs={"data-stat": "franch_name"})]
        team_hrefs = [tag.get("href") for tag in teams_a_tags \
                        if tag is not None]
    
    
    def concat_mapping_fun(href):
        """"""
        return concatenate_href(root_url, 
                                href, 
                                remove_last_dir=True)


    team_links = list(map(concat_mapping_fun, team_hrefs))
    
    # Create team season soup object
    reqs = list(map(requests.get, team_links))
    soups = list(map(lambda req: BeautifulSoup(req.content, "html.parser"), reqs))
    
    # Search for season.
    def find_hrefs(soup):
        """"""
        soup_list = soup.find_all(attrs={"data-stat": "season"})
        to_return = [tag.a.get("href") for tag in soup_list 
                     if tag.a is not None 
                     if re.search(team_season, tag.a.string)]
        if len(to_return) > 0:
            return to_return[0]
        else:
            return None
    
    season_hrefs = list(map(find_hrefs, soups))
    # Update teams vector.
    team_names = [t for i, t in enumerate(team_names) 
                  if season_hrefs[i] is not None]
    season_hrefs = [s for s in season_hrefs if s is not None]
    season_links = list(map(concat_mapping_fun, season_hrefs))
    
    # Create team soup object
    reqs = list(map(requests.get, season_links))
    soups = list(map(lambda req: BeautifulSoup(req.content, "html.parser"), reqs))
    
    # td tags containing players info. 
    def find_roster_tds(soup):
        """"""
        soup_list = soup.find_all("td", attrs={"data-stat": "player"})
        to_return = [td for td in soup_list if is_roster_descendant(td)]
        return to_return
    
    td_soups = list(map(find_roster_tds, soups))
    
    def retrieve_stats_from_td_soup(td_soup):
        """This is a big function return final stats from previously defined 
        'td_soups' list.
        """
        # Initialize the dictionary that will be filled with each player's stats.
        if players == "all":
            # If the user does not input the explicit list of players's names, that 
            # list needs to be programmatically retrieved.
            # Create a list containing players's name.
            # First, perform the initial soup search.
            players_name = [tag.string for td in td_soup for tag in td]
            # Clean the list from unnecessary elements.
            # Remove Basketball Reference's 'TW' strings.
            players_name = clean_list_TW(players_name)
            # Remove unicode non-breaking whitespaces (\xa0's).
            players_name = [el for el in players_name if not are_there_unicode_nbsp(el)]
            players_dict = {name: [] for name in players_name}
        else:
            players_dict = {name: [] for name in players} # players is the user input.
        
        
        # RETRIEVE STATS FOR EACH PLAYER.
        # First. Compose the address needed for accessing each players' page.
        players_href = [tag.a.get("href") for tag in td_soup if tag.a is not None]
        players_link = [concatenate_href(root_url, p_href, remove_last_dir=True) \
                        for p_href in players_href]
        
        # Second. For each player, create soup object of the page containing the stats 
        # for input 'players_season'.
        #   - Create list of players' soup.
        #       - Create soup from request.
        players_soup = list(map(create_soup_from_url, players_link))
        #   - For each player:
        #       - create link to 'player_season'.
        stats_href = []
        to_remove = []
        for i, p_soup in enumerate(players_soup):
            season_a_tags = [a for th in p_soup.find_all("th", attrs={"data-stat": "season"}) \
                             for a in th if a.string == players_season]
            if len(season_a_tags) > 0:
                a_tag = season_a_tags[0]
                stats_href.append(a_tag.get("href"))
            else:
                to_remove.append(players_name[i])
        
        players_name = [p for p in players_name if p not in to_remove]
        
        stats_link = [concatenate_href(root_url, s_href, remove_last_dir=True) \
                      for s_href in stats_href]
        
        #       - create soup object of the page containing the actual stats.
        stats_soup = list(map(create_soup_from_url, stats_link))
        
        # Create table with id for regular season and playoffs.
        # This keys will be used for soup-searching the tables contaning the stats for 
        # the regular season and/or the playoffs (depending on the given user input).
        table_id_dict = {
                "regular": "pgl_basic",
                "playoffs": "pgl_basic_playoffs",
                "both": ["pgl_basic", "pgl_basic_playoffs"]
                }
        tbl_ids = table_id_dict[time_of_season]
        
        # Create season iterator.
        if time_of_season == "both":
            season_times = ["regular", "playoffs"]
            season_iterator = tuple(zip(tbl_ids, season_times))
        else:
            tbl_ids = [tbl_ids,] # for proper zipping.
            season_times = [time_of_season,]
            season_iterator = tuple(zip(tbl_ids, season_times))
            
        # Initialize the table that will contain the tables for regular season and/or
        # playoffs (depending on the given user input).
        table_dict = {k: [] for k in season_times}
        
        to_remove = {k: [] for k in season_times}
        for (season_time_id, season_time) in season_iterator:
            #       - extract table of stats
            stats_tables = [extract_table(soup, table_id=season_time_id) \
                            for soup in stats_soup]
            if season_time == "regular":
                for i, tbl in enumerate(stats_tables):
                    if len(tbl) == 0:
                        to_remove[season_time].append(players_name[i]) # has not stats in 
                        # 'season_time'.
                        stats_tables.pop(i)
            # For playoffs stats, we need to extract stats from Comment elements. 
            if season_time == "playoffs": 
                is_comment = lambda text: isinstance(text, Comment)
                find_comments = lambda s: s.find_all(string=is_comment)
                comments_list = list(map(find_comments, stats_soup))
                detect_playoffs_id = lambda comment: 'id="pgl_basic_playoffs"' \
                in comment.string
                tag_from_comment = lambda comment: BeautifulSoup(comment, "html.parser")     
                stats_tables = []
                for i, comments in enumerate(comments_list):
                    to_remove_flag = True # Default
                    for comment in comments:
                        if detect_playoffs_id(comment):
                            stats_tables.append(tag_from_comment(comment))
                            to_remove_flag = False
                            break
                    if to_remove_flag:
                        to_remove[season_time].append(players_name[i])
               
                
            # Remove players for which no stats where found. 
            players_with_stats = [p for p in players_name if p not in to_remove[season_time]]
                        
            # Extract names of stats
            if len(stats_tables) == 0:
              return("exception!")
          
            stats_names_container = stats_tables[0].find(lambda tag: 
                                                         tag.name=="tr" and
                                                         tag.parent.name=="thead")
            stats_names = [stat.string for stat in stats_names_container.find_all("th")]
            # Clean unicode non-breaking whitespaces.
            #stats_names = [el for el in stats_names if not are_there_unicode_nbsp(el)]
            # Fix some stats' name. 
            stats_names[7] = "Win_Loss"
            
            # Initilize the dictionary containing the stats of each player.
            players_stats = {}
            # Fill it roughly with the stats. Values of the dictionary will be refined 
            # later.
            for i, name in enumerate(players_with_stats):
                table = stats_tables[i]
                stats = table.find_all("tr", id=re.compile("pgl_basic"))
                players_stats[name] = stats
                
            
            # Extract NavigatingStrings for each player, for each game of the year.
            # For each player:
            #   - Take the stats for the whole season:
            #       - For each game of the season:
            #           - Extract the stats for the game as strings
            for player in players_stats:
                season_games = players_stats[player]
                for i, game in enumerate(season_games):
                    missing_indexes = missing_stats_index(game)
                    game_stats = game.find_all(attrs={"data-stat": True})
                    game_stats = [g for g in game if len(g) > 0]
                    game_stats = [[stat.string for stat in stats] for stats in game_stats]
                    for index in missing_indexes:
                        game_stats.insert(index, " ")
                    season_games[i] = game_stats
                players_stats[player] = season_games
            
            
            # Check for the presence of games being described by less than 30 stats (the
            # number of columns).
            # For each player of the team.
            are_30_stats_dict = {player: [] for player in players_with_stats}
            
            for player, season_stats in players_stats.items():
                for game_stat in season_stats:
                   are_30_stats_dict[player].append(are_30_stats(game_stat))
                   
            # "Short stats" meaning less than 30 stats are available.  
            has_player_short_stats = list(map(lambda x: not all(x), 
                                              are_30_stats_dict.values()))
            print("Are there players with short stats?: {}".format("Yes" \
                  if any(has_player_short_stats) else "No"))
            
            # Arrange stats in a table form, for each player, creating a pandas dataframe.
            for player, season_stats in players_stats.items():
                unlisted_stats = [[stat for listed_stat in game_stats \
                                   for stat in listed_stat] \
                                   for game_stats in season_stats]
                players_stats[player] = pd.DataFrame(unlisted_stats, 
                                                     columns=stats_names)
                players_stats[player].set_index("Date", inplace=True)
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
        def concatenate_season_times(player_name):
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
        stats_dict = {k: [] for k in players_name}  
        for p in players_name:
            if time_of_season == "both":
                stats_dict[p] = concatenate_season_times(p) 
            else:
                if p not in table_dict[time_of_season].keys():
                    continue
                stats_dict[p] = table_dict[time_of_season][p]
                
        print("OK")
        
        return stats_dict
    
    to_return_dict = {}
    for i, soup in enumerate(td_soups):
        to_return_dict[team_names[i]] = retrieve_stats_from_td_soup(soup)

    return to_return_dict
    
    
    
    
    
