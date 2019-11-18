import numpy as np
from textblob import TextBlob
import sqlite3


import flask
import requests





# i need asr code to generate speech and send it to a server with a timestamp along with the direction of sound at the time
    #an endpoint to save it to a words table


@app.route('/word/', methods=['GET', 'POST'])
def log_word():
    w = request.form['word']
    d = request.form['direction']
    conn = sqlite3.connect('database.db')


#query latest convo 
    #type of query
@app.route('/lastConvo/', methods=['GET', 'POST'])
def last_convo():
    angleOfhead = 33
    angleTolerance = 5
    secondsToEndConvo = 100
    
    t = request.form['type']
    #pull last thousand words 
    #parse for speaker and convo
    conn = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT user_id, MAX(created_at) FROM objects GROUP BY user_id")
    rows = cur.fetchall()

    #iterate though the rows
    convo = []
    i=0
    interval = 0
    lastTime = rows[0].time
    while(row[i].time - lastTime < secondsToEndConvo):
        if(abs(row[i].angle - angleOfhead) > angleTolerance):
            lastTime = row[i].time
        convo.append(rows[i])
        i = i + 1

    #seperate the words you said from the ones they said based on the angle of incedence
    you = []
    them = []
    for w in convo:
        if(abs(w.angle - angleOfhead) > angleTolerance):
             you.append(w.word)
        else:
                them.append(w.word)

        #convert list to strings
        youStr = ""
        themStr = ""
        for w in you:
            youStr = youStr + " " + w

        for w in them:
            themStr = themStr + " " + w

        #return a word describing the sentiment
        if(t == "i"):
            p = TextBlob(youStr).sentiment.polarity
            if(p>.25):
                return "positive"
            if(p<-.25):
                return "negitive"
            return "pretty neutral"

        if(t == "them"):
            p = TextBlob(themStr).sentiment
            if(p>.25):
                return "positive"
            if(p<-.25):
                return "negitive"
            return "pretty neutral"





