# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 00:47:00 2021

@author: pmjum
"""

from flask import Flask
from threading import Thread

app = Flask('')

@app.route("/")
def home():
  return "Hello, I am still alive"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()