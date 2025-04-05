from pymongo import MongoClient
import pandas as pd

CONNECTION_STRING = "mongodb://mongodb:mdmproj1@mongodbclusterproj1.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"

client = MongoClient(CONNECTION_STRING)

db = client["energiedaten"]
collection = db["stromdaten"]

df = pd.read_csv("data/processed/stromdaten.csv")

# Optional: Fehlende Werte ersetzen
df = df.fillna("")

collection.insert_many(df.to_dict("records"))

print("✅ Upload erfolgreich!")

