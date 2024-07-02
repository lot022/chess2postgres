# chess2postgres 

Simple python library to fetch games directly into Postgres database from Lichess.org using it's API or pgn file containing games.

# Installation.

      $ pip install chess2postgres

# Usage.

      from chess2postgres import lichess_pgn2db, lichess_api2db

# About.

Main goal while creating this library was creating possibility of fetching chess games directly into your Postgres database as chess games db's  are getting popular lately.

# Worth knowing.

Lichess API and pgn files may differ a little in some aspects. One of them is termination - while using api to fetch games, end of the game is descirbed more precisely - mate, resign, out of time, variant end (in RacingKings for example). On the other hand, pgn files call them 'abandoned', 'time forfeit' and 'standard'. I decided not to mess with it and leave it how it is. Despite this fact, it is possible to keep both games from pgn files and those fetched directly from Lichess in a same db.

# Functions.

Currently, library supports 2 formats of inserting data into the database. You can do it from pgn file already downloaded and stored on your device or you can use Lichess API to directly fetch games from Lichess.org into the database. 


### lichess_pgn2db 

This function works when you have already downloaded pgn file from Lichess.org and want to fetch it into the database.
To sucesfully call this function, you have to specify parameters such as:

- dbname : Name of the database in Postgres.
- user : Name of the database user.
- password : User's assword to the database.
- host : Host of the database. 
- port : Port of the database.
- pgn : A path to the pgn file stored on your device.

Predefined parameters:

- tablename : name of the table to which you want to insert all the data. By default it creates a new table called 'lichess_games'.


By default, Lichess pgn files contain '?' in situations where a data is missing. It can happen when the game was abandoned (opening, ECO code, are marked as '?' and the game is just a empty string) or one of the players did not have an account (name, elo, RatingDiff are marked as '?'). In situatuons where the pgn file contains '?', it is added to the database this way. On the other hand, when the data is lacking (for example pgn file does not contain info about openings), they are marked as 'unknown'. Thats why some of the columns are labeled as text, even they could be integer or boolean. 



### lichess_api2db

This function is useful when you want to fetch games directly from Lichess to your database without downloading the pgn file. Sucesfull call of this function requires passing parameters such as:

- dbname : Name of the database in Postgres.
- user : Name of the database user.
- password : User's password to the database.
- host : Host of the database. 
- port : Port of the database.
- api_token : Your Lichess API token
- player_name : Account name of player whose games you want to fetch.
- amount : Amount of games to be fetched into the db.

Predefined parameters: 
- tablename: name of the table to which you want to insert all the data. By default it creates a new table called 'lichess_games'
- perf_type : Type of the games (blitz,bullet,rapid) you want to fetch. Default is None.
- color : Color of pieces that the player has played the games with. Default is None.
- pgn_moves : If true, the game will contain move chars (1.e4 e5 2.Nf3 Nf6). If false, the game will not contain them at all. Default is True.
- rated : If True, the games will be rated. If False, the games will be unrated. Default is None.


Same as in lichess_pgn2db, this func describes all data that is lacking as 'unknown'. Consider that sometimes opening, ECO etc are not appropiate due to gametype.

sample usage:

       lichess_api2db('postgres', 'postgres', 'pass123','localhost', 5432, 'api_token777', 'Player01', 5, tablename='rapid_games', perf_type='rapid', rated='True')


It connects to the db, fetches 'Player01' rapid, ranked games from Lichess to your Postgres databse using specified api token. Done.
