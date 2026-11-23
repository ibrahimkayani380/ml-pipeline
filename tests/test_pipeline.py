import json
from pathlib import Path
from fastapi.testclient import TestClient
import app as appmod

cfg = json.loads(Path("config.json").read_text())

def test_metrics_file():
    m = json.loads(Path("artifacts/metrics.json").read_text())
    assert m["student_id"] == cfg["student_id"]
    assert 0 < m["accuracy"] <= 1
    assert m["training_rows"] >= 100

def test_api():
    c = TestClient(appmod.app)
    assert c.get("/metrics").status_code == 200
    rec = {f: 0.0 for f in cfg["features"]}
    r = c.post("/predict", json={"records": [rec]})
    assert r.status_code == 200 and len(r.json()["predictions"]) == 1
