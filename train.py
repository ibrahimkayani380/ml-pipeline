import json, os, hashlib, yaml, joblib, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

cfg = yaml.safe_load(open("config.yaml"))
path = cfg["dataset"]
sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
df = pd.read_csv(path)
X, y = df.drop(columns=[cfg["target"]]), df[cfg["target"]]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
m = RandomForestClassifier(n_estimators=cfg["n_estimators"],
                           max_depth=cfg["max_depth"], random_state=42).fit(Xtr, ytr)
acc = accuracy_score(yte, m.predict(Xte))
joblib.dump(m, "model.pkl")
out = {"student_id": cfg["student_id"], "accuracy": round(acc, 6),
       "training_rows": len(Xtr), "model_version": sha[:12],
       "dataset_sha256": sha, "git_sha": os.environ.get("GIT_SHA", "unknown")}
json.dump(out, open("metrics.json", "w"))
print(out)
