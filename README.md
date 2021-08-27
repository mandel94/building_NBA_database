# building_NBA_database
The aim of this project is the creation of a database of NBA statistics. 

Statistics are retrieved from the website https://www.basketball-reference.com/. 
This website is a great source of information relating NBA teams, players and seasons over the years. I would like to retrieve that information using web-scraping tools, 
with the objectives of:
1. refactoring  that information to dataframes data structures.
2. organizing the resulting data structures into a relational database. 


Tools: 
  - Beautiful Soup (version 4.9.3) for web-scraping.
  - MySQL (8.0.25 MySQL Community Server) for creating the database.


Programming Languages:
  - Python (version 3.9)
 
 

## Glossary of stat table:
    player_name -- Name of the player
    ranker -- Rank
    game_season -- Season Game
    date_game -- Game Date
    age -- Player's age on February 1 of the season
    team_id -- Team
    game_location -- 'Home' vs 'Away'
    opp_id -- Opponent
    net_score -- net difference of final score (`+` if the player's team won)
    win_loss -- Did the player's team won? 
    gs -- has the player played from start of the game? 
    mp -- Minutes Played
    fg -- Field Goals
    fga -- Field Goal Attempts
    fg_pct -- Field Goal Percentage
    fg3 -- 3-Point Field Goals
    fg3a -- 3-Point Field Goal Attempts
    fg3_pct -- 3-Point Field Goal Percentage
    ft -- Free Throws
    fta -- Free Throw Attempts
    ft_pct -- Free Throw Percentage
    orb -- Offensive Rebounds
    drb -- Defensive Rebounds
    trb -- Total Rebounds
    ast -- Assists
    stl -- Steals
    blk -- Blocks
    tov -- Turnovers
    pf -- Personal Fouls
    pts -- Points
    game_score -- Game Score (https://www.nbastuffer.com/analytics101/game-score/  for more infos)
    +/- -- Plus/Minus
