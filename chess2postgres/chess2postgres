import psycopg2
import chessanalytics
import berserk
import datetime

# why not one func for every platform, or even one func for all? 
# i did not want user to set too many variables, make him/her check if they are correct etc and just frustrate all users.

# despite slightly different possible outputs for png and api fetched games, I decided to make them have same layout and make it possible to store games fetched using api and from 
# pgn files in the same table.

def lichess_pgn2db(dbname : str, user : str, password: str, host : str, port : int, pgn : str, tablename : str='lichess_games'):
    '''
    Function that fetches games from pgn file and stores them in your Postgres database.

    Params:
    dbname : str : Name of the database
    user : str : Name of the user
    password : str : Password of the user
    host : str : Host of the database
    port : int : Port of the database
    pgn : str : Path to the pgn file
    san_notation : bool : If True, games will be stored in SAN notation. If False, games will be converted into LAN notation before being added to db. 
    Default is True.
    tablename : str : Name of the table where you want to store the games. Default is 'lichess_games'.
    '''

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    cursor,ca = conn.cursor(),chessanalytics.CA(pgn, '')

    gierki = ca.get_all()

# some cols are labeled text even if they could be other type (bool, int etc) because you dont know if it will be described normally or as '?' or 'unknown' 
# or will not be described at all,  and just leaving it like that may cause some unwanted errors.

    cursor.execute('CREATE TABLE IF NOT EXISTS %s('
                   'event TEXT, white TEXT, black TEXT, white_elo TEXT, black_elo TEXT, WhiteRatingDiff TEXT, BlackRatingDiff TEXT, result TEXT, date DATE, time TIME, lichess_game_ID TEXT, time_control TEXT, eco TEXT, opening TEXT, variation TEXT, termination TEXT, ranked TEXT, game TEXT);' % (tablename,))

    for v in gierki.values():
        cursor.execute(f"INSERT INTO {tablename} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s);",
                (v['event'], v['white'], v['black'], v['white_elo'], v['black_elo'], v['WhiteRatingDiff'], v['BlackRatingDiff'], v['result'], 
                 v['utcdate'], v['utctime'], v['game_id'], v['timecontrol'], v['eco'], v['opening'], v['variant'], v['termination'], v['ranked'] ,v['game']))

    # I decided that games should be the last argument due to different game lengths. It looks better in PgAdmin and is easier to read.

    conn.commit() 

    cursor.close()
    conn.close()



# after creating all of it i thought about fetching games with as_pgn=True param and get the data same way as I do in pgn. may change it in the future

def lichess_api2db(dbname : str , user : str, password : str, host : str, port : int, api_token : str, player_name : str , amount : int, tablename='lichess_games', perf_type=None, color=None,
                   pgn_moves : bool = True, rated : bool =None, opponent : str =None):
    '''
    Function that uses Lichess API to fetch games directly to your Postgres database.

    Params:
    dbname : str : Name of the database
    user : str : Name of the user
    password : str : Password of the user
    host : str : Host of the database
    port : int : Port of the database
    api_token : str : Your Lichess api token
    player_name : str : Name of the player whose games you want to fetch.
    amount : int : Amount of games to fetch. Must be a integer higher or equal 2.
    tablename : str : Name of the table where you want to store the games. Default is 'lichess_games'.
    perf_type : str : Type of the games (blitz,bullet,rapid) you want to fetch. Default is None (all types).
    color : str : Color of pieces that the player has played the games with. Default is None (both black and white).
    rated : bool : If True, the games will be rated. If false, the games will be unrated. Default is None.
    pgn_moves : bool : If True, the games will contain move chars (1. e4 d5 2. exd5 Nf6). If False, they will not (e4 d5 exd5 Nf6). By default set to True.
    opponent : str : Determines if fetched games should be against specified opponent. By default is set to None (all opponents)
    '''


    def create_data(el):

        # dlugosv 1 pa,ietac zmienic bo error  / fixed

        d, i = {}, 0

        for e in el:

            i += 1

            d[str(i)] = {}
            for k,v in e.items():

                if k == 'id':
                    d[str(i)]['game_id'] = v

                elif k == 'rated':
                    d[str(i)]['ranked'] = v

                elif k == 'variant':
                    d[str(i)]['variant'] = v

                
        # decided to create it by myself, did not want to leave it unknown or just call it blitz, bullet etc.
                elif k == 'speed':
                    x = 'Ranked' if d[str(i)]['ranked'] == True else 'Unranked'
                    d[str(i)]['timecontrol'] = x + ' ' + v + ' ' + d[str(i)]['variant'] + ' ' + 'game'

                elif k == 'status':
                    d[str(i)]['termination'] = v

                elif k == 'players':
                    d[str(i)]['white'] = v['white']['user']['name']
                    d[str(i)]['black'] = v['black']['user']['name']
                    d[str(i)]['white_elo'] = v['white']['rating']
                    d[str(i)]['black_elo'] = v['black']['rating']

                    try:
                        d[str(i)]['WhiteRatingDiff'] = v['white']['ratingDiff']
                        d[str(i)]['BlackRatingDiff'] = v['black']['ratingDiff']

                    except KeyError:
                        d[str(i)]['WhiteRatingDiff'] = 'unknown'
                        d[str(i)]['BlackRatingDiff'] = 'unknown'

                # decided to take creation date as 'UTCdate' in pgn.

                elif k == 'clock':
                    d[str(i)]['time'] = str(v['initial']) + '+' + str(v['increment'])

                elif k == 'createdAt':

                    x = datetime.date(v.year, v.month, v.day)
                    y = datetime.time(v.hour, v.minute, v.second)
    
                    d[str(i)]['utcdate'] = x.strftime("%Y-%m-%d")
                    d[str(i)]['utctime'] = y.strftime("%H:%M:%S")

                elif k == 'winner':
                    x = '1-0' if v == 'white' else '0-1' if v == 'black' else '1/2-1/2'
                    d[str(i)]['result'] = x

                elif k == 'opening':

                    try:
                        d[str(i)]['opening'] = v['name']
                        d[str(i)]['eco'] = v['eco']

                    except KeyError:

                        d[str(i)]['opening'] = 'unknown'
                        d[str(i)]['eco'] = 'unknown'

                elif k == 'moves':
                    d[str(i)]['game'] = v   


            elements = ['event', 'white', 'black', 'white_elo', 'black_elo', 'WhiteRatingDiff', 'BlackRatingDiff', 'result', 'date', 
                        'time', 'lichess_game_ID', 'time_control', 'eco', 'opening', 'variation', 'termination', 'ranked', 'game']


            for v in d.values():
                for e in elements:
                    if e not in v:
                        v[e] = 'unknown'


        ## koty koteczki  
        ## koty koteczki  

        return d
    
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    session = berserk.TokenSession(api_token)
    client = berserk.Client(session=session)

    imported = client.games.export_by_player(player_name,as_pgn=False,max=amount, opening=True, perf_type=perf_type, color=color, rated=rated, moves=pgn_moves, vs=opponent)

    cursor = conn.cursor()

    dt = create_data(imported)

    cursor.execute('CREATE TABLE IF NOT EXISTS %s('
                   'event TEXT, white TEXT, black TEXT, white_elo TEXT, black_elo TEXT, WhiteRatingDiff TEXT, BlackRatingDiff TEXT, result TEXT, date TEXT, time TEXT, lichess_game_ID TEXT, time_control TEXT, eco TEXT, opening TEXT, variation TEXT, termination TEXT, ranked TEXT, game TEXT);' % (tablename,))

    for v in dt.values():
        cursor.execute(f"INSERT INTO {tablename} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s,%s);",
            ( v['timecontrol'], v['white'], v['black'], v['white_elo'], v['black_elo'], v['WhiteRatingDiff'], v['BlackRatingDiff'], v['result'], 
             v['utcdate'], v['utctime'], v['game_id'], v['time'], v['eco'], v['opening'], v['variant'], v['termination'], v['ranked'] ,v['game']))

    conn.commit()
    cursor.close()
    conn.close()

