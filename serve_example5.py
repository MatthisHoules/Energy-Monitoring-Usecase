# External Imports
import json
from flask import jsonify, make_response


# Internal Imports
from src.App.EnergyMonitorApp import EnergyMonitorApp

def fibonacci(n):
    if(n <= 1):
        return n
    else:
        return (fibonacci(n-1) + fibonacci(n-2))
# def fibonacci(n)


app = EnergyMonitorApp(
    "0.0.0.0",
    8084,
    "t5",
    "config.json"
)


@app.route("/fibo/<int:n>/<int:i>", methods=["GET"], monitored_params={
    "n" : [5, 15],
    "i" : [5, 20]
})
def fibo(n : int, i : int):
    for _ in range(i) :
        ct = fibonacci(n)
    
    response = make_response(jsonify({f"Fibanicci, n={n}:" :  ct}), 200)
    
    return response
# def fibo(n : int, i : int)



@app.route("/test/<int:n>", methods=["GET"], monitored_params={
    "n" : [5, 10]
})
def route2(n : int):
    ct = fibonacci(n)
    
    response = app.app.response_class(
        response=json.dumps({f"Fibanicci, n={n}:" :  ct}),
        status=200,
        mimetype='application/json'
    )
    
    return response
# def route2(n : int)



@app.route("/", methods=["GET"])
def index():
    response = app.app.response_class(
        response=json.dumps("index"),
        status=200,
        mimetype='application/json'
    )
    
    return response
# def index()


app.run()