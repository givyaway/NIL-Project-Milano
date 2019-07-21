import json
import mysql.connector
import random
from datetime import date, datetime, timedelta
import ast

class Database:
    def __init__(self):
        host = HOST
        user = USER
        password = PWD
        db = DB
        self.con =  mysql.connector.connect(host=host, user=user, password=password, db=db, charset='utf8')
        self.cur = self.con.cursor(dictionary=True)
        self.con.autocommit = True
    def get_avg_votes(self):
        query = ("""SELECT n.id id_nil, t.avg_vote1, t.avg_vote2, t.avg_vote3, t.avg_vote4, (t.avg_vote1 + t.avg_vote2 + t.avg_vote3 + t.avg_vote4)/4 avg_rate, t.nvotes
                    FROM NIL n
                    LEFT JOIN (SELECT id_nil, AVG(vote1) avg_vote1, AVG(vote2) avg_vote2, AVG(vote3) avg_vote3, AVG(vote4) avg_vote4, count(ip) as nvotes
                    FROM votes
                    GROUP BY id_nil) as t ON t.id_nil = n.id"""
                 )
        self.cur.execute(query)
        result = self.cur.fetchall()
        return str(result)

# aggiornamento file geojson e media voti
def main():
    filename = 'nilzone2.geojson'
    db = Database()
    try:
        r = db.get_avg_votes()
    except mysql.connector.errors.IntegrityError as e:
        return "ERROR"
    list_votes = ast.literal_eval(r)
    
    with open(filename, 'r') as f:
        geojson = json.load(f)    
        for nil in list_votes:
            for feature in geojson["features"]:
                if nil['id_nil'] ==  feature["properties"]['ID_NIL']:
                    if nil['avg_rate'] is not None:
                        feature["properties"]["rating"] = round(nil['avg_rate'], 2)
                    else:
                        feature["properties"]["rating"] = None
                    break
        with open(filename, 'w') as outfile:  
            json.dump(geojson, outfile)
    
    filename2 = 'read_votes.json'
    with open(filename2, 'w') as outfile:  
        json.dump(list_votes, outfile)
        
    
        
if __name__ == '__main__':
    main()
