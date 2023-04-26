#!/usr/bin/env python
# encoding: utf-8

from joulehunter import Profiler
from flask import Flask
import json
from EnergyMonitoring import EnergyMonitoring
import requests

def fibonacci(n):
    if(n <= 1):
        return n
    else:
        return (fibonacci(n-1) + fibonacci(n-2))
# def fibonacci(n)

app = Flask(__name__)


@EnergyMonitoring(app, n = [20, 15])
@app.route('/<int:n>')
def index(n : int):
    ct = fibonacci(n)
    
    response = requests.get('http://127.0.0.1:9091/5') 
    print(response)

    return json.dumps({"Fibanicci, n=20:" :  ct})
# def index(n : int)


@EnergyMonitoring(app, n = [10, 5])
@app.route('/fibo/<int:n>')
def fibo(n : int):
    ct = fibonacci(n)
    
    
    
    response = app.response_class(
        response=json.dumps({"Fibanicci, n=20:" :  ct}),
        status=300,
        mimetype='application/json'
    )
    return response
# def fibo(n : int)



from requests_html import HTMLSession
from wsgiadapter import WSGIAdapter

s = HTMLSession()
s.mount("http://test", WSGIAdapter(app))

r = s.get("http://test/fibo/5")
print(r.content)