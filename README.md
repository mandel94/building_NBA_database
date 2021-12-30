# building_NBA_database
The aim of this project is the creation of a database of NBA statistics. 
Starting from web-scraping this wonderful basketball website (https://www.basketballreference.com/), the objective is to develop a program in Python that allows me to organize in a database all available statistics about players, teams and seasons. I would then organize the data in a RDBMS (MySQL), getting a historical NBA archive at my disposal for future sport analytics projects.  

Basketball Reference is a great source of statistics about NBA teams, players and seasons. I would like to retrieve that information using web-scraping tools, 
with the objectives of:
1. refactoring  that information into dataframes data structures;
2. organizing the resulting data structures with a relational database management system. 


Tools: 
  - Beautiful Soup (version 4.9.3) for web-scraping.
  - MySQL (8.0.25 MySQL Community Server) for creating and managing the database.


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
