#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
import json
from EnergyMonitoring import EnergyMonitoring

def fibonacci(n):
    if(n <= 1):
        return n
    else:
        return (fibonacci(n-1) + fibonacci(n-2))
# def fibonacci(n)



app = Flask(__name__)


@EnergyMonitoring("index", "/<int:n>", 20, n=[20, 15])
@app.route('/<int:n>')
def index(n : int):
    ct = fibonacci(n)
    
    return json.dumps({"Fibanicci, n=20:" :  ct})
# def index(n : int)


@EnergyMonitoring("fibo", "/fibo/<int:n>", 20, n=[10, 5])
@app.route("/fibo/<int:n>")
def fibo(n : int):
    ct = fibonacci(n)
    
    response = app.response_class(
        response=json.dumps({"Fibanicci, n=20:" :  ct}),
        status=300,
        mimetype='application/json'
    )
    
    return response
# def fibo(n : int)


if __name__ == "__main__" :
    app.run()