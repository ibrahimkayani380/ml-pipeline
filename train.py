import json, joblib, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
df = pd.read_csv("data/dataset.csv")
X, y = df.drop(columns=["label"]), df["label"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
m = RandomForestClassifier(n_estimators=100, max_depth=1, random_state=42).fit(Xtr, ytr)
acc = accuracy_score(yte, m.predict(Xte))
joblib.dump(m, "model.pkl")
json.dump({"accuracy": round(acc, 4)}, open("metrics.json", "w"))
print("accuracy", acc)
