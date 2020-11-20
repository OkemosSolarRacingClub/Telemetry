from __future__ import division
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()

from flask import Flask, render_template, redirect, request, url_for
import re
import socket
import os
import requests
import json
import pyrebase
import datetime
import random
import decimal
from bs4 import BeautifulSoup
import lxml

app = Flask(__name__)

config = {
    "apiKey": "api key",
    "authDomain": "firebase-url.firebaseio.com/",
    "databaseURL": "https://firebase-url.firebaseio.com/",
    "storageBucket": "",
    "serviceAccount": "credentials-file.json"
}


def dbinit():
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db


@app.route('/message', methods=['POST'])
def message():
    msg = request.form.get("msg")
    if msg is not None and msg != "":
        db = dbinit()
        db.update({'message': msg})
    return 'Thank you :)'


@app.route('/warning', methods=['POST'])
def warning():
    msg = request.form.get("msg")
    if msg is not None and msg != "":
        db = dbinit()
        db.update({'caution': msg})
    return 'Thank you :)'


@app.route('/send')
def sendmsg():
    return render_template('send.html')


@app.route('/caution')
def caution():
    return render_template('caution.html')


@app.route('/dashboard')
def dashboard():
    return render_template('car.html')


@app.route('/')
def home():
    return render_template('public.html')


@app.route('/lap')
def laps():
    url = "https://api.solarcarchallenge.org/pages/scores/"

    headers = {
        'Accept': "*/*",
        'Host': "api.solarcarchallenge.org",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive"
    }

    response = requests.request("GET", url, headers=headers)

    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    p = soup.find_all('tr')
    okemos = None
    for tr in p:
        if 'Okemos' in tr.text:
            okemos = tr
            break

    if okemos is not None:
        db = dbinit()
        db.update({'laps': okemos.find_all('td')[5].text})
        db.update({'cumlaps': okemos.find_all('td')[6].text})
    return 'all good'


@app.route('/rpi', methods=['POST'])
def rpi():
    pw = request.form.get("pw")
    s = request.form.get("s")
    t = request.form.get("t")
    rpiip = request.form.get("i")
    v = request.form.get("v")
    ba = request.form.get("ba")
    if pw == "this is our password":
        if s is not None or t is not None or rpiip is not None or v is not None or ba is not None:
            db = dbinit()
            if s is not None:
                db.update({'speed': s})
                sint = float(s)
                if 30 > sint > 0:
                    datapoints = int(db.child("datapoints").get().val()) + 1
                    speedtotal = float(db.child("speedtotal").get().val()) + sint
                    db.update({'datapoints': datapoints})
                    db.update({'speedtotal': speedtotal})
                    db.update({'avgspeed': round((speedtotal/datapoints), 2)})
                ampspeed = sint
                amp = int(db.child("amp").get().val())
                if ampspeed < 13:
                    amp = 0
                elif ampspeed < 14:
                    amp = random.randint(6, 12)
                elif ampspeed < 15:
                    amp = random.randint(10, 25)
                elif ampspeed < 20:
                    amp = random.randint(17, 24)
                elif ampspeed < 30:
                    amp = random.randint(23, 55)
                elif ampspeed < 40:
                    amp = random.randint(34, 80)
                db.update({'amp': amp})
                if t is not None:
                    if t == "reset":
                        db.update({'trip_distance': 0})
                        return "Reset and ready!"
                    elif int(t) > 0:
                        odo = int(db.child("odometer").get().val()) + (66 * int(t))
                        db.update({'odometer': odo})
                        td = int(db.child("trip_distance").get().val()) + (66 * int(t))
                        db.update({'trip_distance': td})
            if rpiip is not None:
                db.update({'rpiip': rpiip})
            if v is not None:
                db.update({'charge': v})
            if ba is not None:
                db.update({'battery-amperage': ba})
            db.update({'last_update': str(datetime.datetime.utcnow())})
            return "Logged to db"
        return "Speed data is empty"
    return "Incorrect password"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
