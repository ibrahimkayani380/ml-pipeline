from flask import Flask, Response
import json
app = Flask(__name__)
@app.route("/")
def home(): return "ML app running"
@app.route("/metrics")
def metrics():
    return Response(json.dumps(json.load(open("metrics.json"))), mimetype="application/json")
app.run(host="0.0.0.0", port=8000)
