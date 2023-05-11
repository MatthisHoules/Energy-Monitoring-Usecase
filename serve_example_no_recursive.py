# External Imports
import json


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
    8080,
    "t1",
    "config.json"
)

@app.route("/fibo/<int:n>/<int:i>", methods=["GET"], monitored_params={
    "n" : [5, 10],
    "i" : [1, 5]
})
def fibo(n : int, i : int):
    result = 0
    for _ in range(i) :
        result += fibonacci(n)
    
    response = app.app.response_class(
        response=json.dumps({f"Fibanicci, n={n} and i={i}:" :  result}),
        status=200,
        mimetype='application/json'
    )
    
    return response
# def fibo(n : int, i : int)



# @app.route("/test/<int:n>", methods=["GET"], monitored_params={
#     "n" : [5, 10]
# })
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
