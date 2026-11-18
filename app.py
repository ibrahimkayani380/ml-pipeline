from flask import Flask, jsonify
import json
app = Flask(__name__)
@app.route("/")
def home(): return "ML app running"
@app.route("/metrics")
def metrics(): return jsonify(json.load(open("metrics.json")))
app.run(host="0.0.0.0", port=8000)
