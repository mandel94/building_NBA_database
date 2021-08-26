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

  

## Glossary of game table:
    Rk -- Rank
    G -- Season Game
    Age -- Player's age on February 1 of the season
    Tm -- Team
    Opp -- Opponent
    GS -- Games Started
    MP -- Minutes Played
    FG -- Field Goals
    FGA -- Field Goal Attempts
    FG% -- Field Goal Percentage
    3P -- 3-Point Field Goals
    3PA -- 3-Point Field Goal Attempts
    3P% -- 3-Point Field Goal Percentage
    FT -- Free Throws
    FTA -- Free Throw Attempts
    FT% -- Free Throw Percentage
    ORB -- Offensive Rebounds
    DRB -- Defensive Rebounds
    TRB -- Total Rebounds
    AST -- Assists
    STL -- Steals
    BLK -- Blocks
