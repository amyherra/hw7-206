
# Your name: Amy Rodriguez
# Your student id:95895844
# Your email: amyrod@umich.edu
# List who you have worked with on this project:Myself 

import unittest
import sqlite3
import json
import os

def read_data(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_positions_table(data, cur, conn):
    positions = []
    for player in data['squad']:
        position = player['position']
        if position not in positions:
            positions.append(position)
    cur.execute("CREATE TABLE IF NOT EXISTS Positions (id INTEGER PRIMARY KEY, position TEXT UNIQUE)")
    for i in range(len(positions)):
        cur.execute("INSERT OR IGNORE INTO Positions (id, position) VALUES (?,?)",(i, positions[i]))
    conn.commit()

## [TASK 1]: 25 points
# Finish the function make_players_table

#     This function takes 3 arguments: JSON data,
#         the database cursor, and the database connection object

#     It iterates through the JSON data to get a list of players in the squad
#     and loads them into a database table called 'Players'
#     with the following columns:
#         id ((datatype: int; Primary key) - note this comes from the JSON
#         name (datatype: text)
#         position_id (datatype: integer)
#         birthyear (datatype: int)
#         nationality (datatype: text)
#     To find the position_id for each player, you will have to look up 
#     the position in the Positions table we 
#     created for you -- see make_positions_table above for details.

def make_players_table(data, cur, conn):
    drop_query = "drop table players"
    cur.execute(drop_query)
    table_query = """CREATE TABLE players(id int PRIMARY KEY,name text,position_id int,birthyear int,nationality text);"""
    
    cur.execute(table_query)
    
    for player in data['squad']:
        id = player['id']
        name = player['name']
        position = player['position']
        birthyear = player['dateOfBirth'][0:4]
        nationality = player['nationality']

    
        qury = f"select id from positions where position = '{position}'"
        cur.execute(qury)
        result = cur.fetchall()
        position_id = result[0][0]

        
        insert_qury = f"INSERT INTO players (id, name, position_id, birthyear, nationality) VALUES({id}, '{name}',{position_id},{birthyear},'{nationality}')"
        print(player)
        print(insert_qury)
        cur.execute(insert_qury)
    conn.commit()


## [TASK 2]: 10 points
# Finish the function nationality_search

    # This function takes 3 arguments as input: a list of countries,
    # the database cursor, and database connection object. 
 
    # It selects all the players from any of the countries in the list
    # and returns a list of tuples. Each tuple contains:
        # the player's name, their position_id, and their nationality.

def nationality_search(countries, cur, conn):
    #loop through each country and select this from players where ..country.. 
    new_list = []
    for country in countries:
        select_query = f"select name, position_id, nationality from players where nationality = '{country}'"
        cur.execute(select_query)
        result = cur.fetchall()
        for player in result:
            new_list.append(player)
    return new_list
    # if countries just has England, in 'England' - just a list countries is just a list, England and Spain in ('England', 'Spain')
    #single quotes and commas #logic that replaces the value with the countries in sqlite formatttt #values within brackets to change to whatever u want - 



## [TASK 3]: 10 points
# finish the function birthyear_nationality_search

#     This function takes 4 arguments as input: 
#     an age in years (int), 
#     a country (string), the database cursor, 
#     and the database connection object.

#     It selects all the players from the country passed to the function 
#     that were born BEFORE (2023 minus the year passed)
#     for example: if we pass 19 for the year, it should return 
#     players with birthdates BEFORE 2004
#     This function returns a list of tuples each containing 
#     the player’s name, nationality, and birth year. 


def birthyear_nationality_search(age, country, cur, conn):
    current_year = 2023
    year_cutoff = current_year - age
    select_query = f"SELECT name, nationality, birthyear FROM players WHERE nationality = '{country}' AND birthyear < {year_cutoff}"
    cur.execute(select_query)
    result = cur.fetchall()
    return result

## [TASK 4]: 15 points
# finish the function position_birth_search

    # This function takes 4 arguments as input: 
    # a position (string), 
    # age (int), the database cursor,
    # and the database connection object. 

    # It selects all the players who play the position
    #  passed to the function and
    # that were born AFTER (2023 minus the year passed)
    # for example: if we pass 19 for the year, it should return 
    # players with birth years AFTER 2004
    # This function returns a list of tuples each containing 
    # the player’s name, position, and birth year. 
    # HINT: You'll have to use JOIN for this task.

def position_birth_search(position, age, cur, conn):
    new_tup = []
    birth_year = 2023 - age
    select_query = f"SELECT players.name, positions.position, players.birthyear FROM players JOIN positions ON players.position_id = positions.id WHERE positions.position = '{position}' AND players.birthyear > {birth_year}"
    cur.execute(select_query)
    result = cur.fetchall()
    for player in result:
        new_tup.append(player)
    return result


# [EXTRA CREDIT]
# You’ll make 3 new functions, make_winners_table(), make_seasons_table(),
# and winners_since_search(), 
# and then write at least 2 meaningful test cases for each of them. 

#     The first function takes 3 arguments: JSON data, 
#     the database cursor, and the database connection object.
#     It makes a table with 2 columns:
#         id (datatype: int; Primary key) -- note this comes from the JSON
#         name (datatype: text) -- note: use the full, not short, name
#     hint: look at how we made the Positions table above for an example

#     The second function takes the same 3 arguments: JSON data, 
#     the database cursor, and the database connection object. 
#     It iterates through the JSON data to get info 
#     about previous Premier League seasons (don't include the current one)
#     and loads all of the seasons into a database table 
#     called ‘Seasons' with the following columns:
#         id (datatype: int; Primary key) - note this comes from the JSON
#         winner_id (datatype: text)
#         end_year (datatype: int)
#     NOTE: Skip seasons with no winner!

#     To find the winner_id for each season, you will have to 
#     look up the winner's name in the Winners table
#     see make_winners_table above for details
    
#     The third function takes in a year (string), the database cursor, 
#     and the database connection object. It returns a dictionary of how many 
#     times each team has won the Premier League since the passed year.
#     In the dict, each winning team's (full) name is a key,
#     and the value associated with each team is the number of times
#     they have won since the year passed, including the season that ended
#     the passed year. 

def make_winners_table(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Winners (id INTEGER PRIMARY KEY, name TEXT)")
    data = data['seasons'] #looping over list that corresponds to seasons
    winners_inserted = []
    for individual_season in data:
        if individual_season['winner']: #will only work if something in winner 
            winners_id = individual_season['winner']['id']
            winners_name = individual_season['winner']['name']
            print(individual_season)
            #DO NOT FORGET THE OR IGNORE -- FAST DEBUGGING 
            if winners_id not in winners_inserted: #already there making sure no duplicate
                cur.execute("INSERT or ignore INTO Winners (id, name) VALUES (?, ?)", (winners_id, winners_name))
                winners_inserted.append(winners_id) #now 
    conn.commit()

def make_seasons_table(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Seasons (id INTEGER PRIMARY KEY, winner_id TEXT, end_year INTEGER)")
    data = data['seasons']
    for season in data:
        season_id = season['id']
        winner_name = None
        winner_year = season['endDate'][0:4]
        if season['winner']:
            winner_name = season['winner']['name'] #if something in winner get name, if not move on 
            print(winner_name)
            cur.execute("SELECT id from Winners WHERE name = ?", (winner_name,))
            result = cur.fetchone()
            print(result)
            winner_id = result[0] #first element #actual winner id now
            cur.execute("INSERT or ignore INTO Seasons (id, winner_id, end_year) VALUES (?,?,?)",(season_id,winner_id,winner_year)) #insert or ignore into seasons - not cleanist way - make debugging errors 
    conn.commit()

def winners_since_search(year, cur, conn):
    cur.execute("SELECT s.winner_id, name FROM Seasons as s JOIN Winners as w ON s.winner_id = w.id WHERE s.end_year >= ?",
            (int(year),))
    results = cur.fetchall()
    winners = {}
    # Count the number of wins for each team
    for result in results:
        winner_id = result[0]
        winner_name = result[1]
        if winner_name not in winners:
            winners[winner_name] = 1
        else:
            winners[winner_name] += 1
    return winners
    


class TestAllMethods(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(path+'/'+'Football.db')
        self.cur = self.conn.cursor()
        self.conn2 = sqlite3.connect(path+'/'+'Football_seasons.db')
        self.cur2 = self.conn2.cursor()

    def test_players_table(self):
        self.cur.execute('SELECT * from Players')
        players_list = self.cur.fetchall()

        self.assertEqual(len(players_list), 30)
        self.assertEqual(len(players_list[0]),5)
        self.assertIs(type(players_list[0][0]), int)
        self.assertIs(type(players_list[0][1]), str)
        self.assertIs(type(players_list[0][2]), int)
        self.assertIs(type(players_list[0][3]), int)
        self.assertIs(type(players_list[0][4]), str)

    def test_nationality_search(self):
        x = sorted(nationality_search(['England'], self.cur, self.conn))
        self.assertEqual(len(x), 11)
        self.assertEqual(len(x[0]), 3)
        self.assertEqual(x[0][0], "Aaron Wan-Bissaka")

        y = sorted(nationality_search(['Brazil'], self.cur, self.conn))
        self.assertEqual(len(y), 3)
        self.assertEqual(y[2],('Fred', 2, 'Brazil'))
        self.assertEqual(y[0][1], 3)

    def test_birthyear_nationality_search(self):

        a = birthyear_nationality_search(24, 'England', self.cur, self.conn)
        self.assertEqual(len(a), 7)
        self.assertEqual(a[0][1], 'England')
        self.assertEqual(a[3][2], 1992)
        self.assertEqual(len(a[1]), 3)

    def test_type_speed_defense_search(self):
        b = sorted(position_birth_search('Goalkeeper', 35, self.cur, self.conn))
        self.assertEqual(len(b), 2)
        self.assertEqual(type(b[0][0]), str)
        self.assertEqual(type(b[1][1]), str)
        self.assertEqual(len(b[1]), 3) 
        self.assertEqual(b[1], ('Jack Butland', 'Goalkeeper', 1993)) 

        c = sorted(position_birth_search("Defence", 23, self.cur, self.conn))
        self.assertEqual(len(c), 1)
        self.assertEqual(c, [('Teden Mengi', 'Defence', 2002)])
    
    # test extra credit
    def test_make_winners_table(self):
        self.cur2.execute('SELECT * from Winners')
        winners_list = self.cur2.fetchall()
        expected_winners_list = [(57, 'Arsenal FC'), (59, 'Blackburn Rovers FC'), (61, 'Chelsea FC'),(64,'Liverpool FC'),(65,'Manchester City FC'),(66,'Manchester United FC'),(338,'Leicester City FC')]
        self.assertEqual(winners_list, expected_winners_list)
    
        

    def test_make_seasons_table(self):
        self.cur2.execute('SELECT * from Seasons where end_year >= 2016')
        seasons_list = self.cur2.fetchall()
        expected_seasons_list = [(23,'65',2018), (151,'65',2019), (256,'61',2017), (257,'338',2016), (468,'64',2020),(619,'65',2021)]
        self.assertEqual(seasons_list, expected_seasons_list)
        

    def test_winners_since_search(self):
        winners_dict = winners_since_search('2015', self.cur2, self.conn2)
        expected_winners_dict = {'Manchester City FC': 3, 'Chelsea FC':2, 'Leicester City FC':1 , 'Liverpool FC':1}
        self.assertEqual(winners_dict, expected_winners_dict)
        


def main():

    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    json_data = read_data('football.json')
    cur, conn = open_database('Football.db')
    make_positions_table(json_data, cur, conn)
    make_players_table(json_data, cur, conn)
    conn.close()


    seasons_json_data = read_data('football_PL.json')
    cur2, conn2 = open_database('Football_seasons.db')
    make_winners_table(seasons_json_data, cur2, conn2)
    make_seasons_table(seasons_json_data, cur2, conn2)
    conn2.close()


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
