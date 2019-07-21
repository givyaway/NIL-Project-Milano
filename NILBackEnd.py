from flask import Flask, render_template
from flask import request
from flask import abort
import json
import mysql.connector
from datetime import date, datetime, timedelta
from flask_cors import CORS, cross_origin
from requests import get
from flask import jsonify

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class Database:
    def __init__(self):
        host = HOST
        user = USER
        password = PWD
        db = DB
        self.con =  mysql.connector.connect(host=host, user=user, password=password, db=db, charset='utf8')
        self.cur = self.con.cursor(dictionary=True)
        self.con.autocommit = True
    def insert_vote(self, id_nil, ip, v1=0, v2=0, v3=0, v4=0):
        d = datetime.now()
        query = ("INSERT INTO votes (id_nil, ip, vote1, vote2, vote3, vote4, date_update) "
                 "VALUES(%s, %s, %s, %s, %s, %s, %s)"
                )
        sql_tuple = (int(id_nil), ip, float(v1), float(v2), float(v3), float(v4), d, )
        self.cur.execute(query, sql_tuple)
        result = self.cur.fetchone()
        return result
    def get_total_votes(self):
        query = "SELECT COUNT(DISTINCT ip) AS count FROM votes"
        self.cur.execute(query)
        result = self.cur.fetchone()
        for k in result:
            return str(result[k])
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
    
db = Database()

@app.route('/')
def index():
    return render_template('nilFull.html')

@app.route('/vote', methods=['POST'])
def vote():
    print(request.form)
    try:
        db.insert_vote(request.form['id_nil'], request.form['ip'], request.form['v1'], request.form['v2'], request.form['v3'], request.form['v4'])
    except mysql.connector.errors.IntegrityError as e:
        return abort(403)
    res = db.get_total_votes()
    return res

@app.route('/totalvotes', methods=['GET'])
def total_votes():
    res = db.get_total_votes()
    return res

@app.route('/getvotes', methods=['GET'])
def get_votes():
    try:
        r = db.get_avg_votes()
    except mysql.connector.errors.IntegrityError as e:
        return "ERROR"
    list_votes = ast.literal_eval(r)
    return jsonify(list_votes)

@app.route('/getrating', methods=['GET'])
def get_rating():
    resp = []
    filename = 'nilzone2.geojson'
    filename2 = 'read_votes.json'
    with open(filename, 'r') as f:
        geojson = json.load(f)   
        with open(filename2, 'r') as f2:  
            list_votes = json.load(f2)
            for nil in list_votes:
                for feature in geojson["features"]:
                    j = {}
                    if nil['id_nil'] ==  feature["properties"]['ID_NIL']:
                        if nil['avg_rate'] is not None:
                            feature["properties"]["rating"] = round(nil['avg_rate'], 2)
                            j['id_nil'] = feature["properties"]['ID_NIL']
                            j['avg_rate'] = round(nil['avg_rate'], 2)
                            resp.append(j)
                        else:
                            feature["properties"]["rating"] = None
                            j['id_nil'] = feature["properties"]['ID_NIL']
                            j['avg_rate'] = None
                            resp.append(j)
                        break
    return jsonify(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
