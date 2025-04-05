from pymongo import MongoClient
import pandas as pd
import sys

# Verbindung aus Kommandozeilenargument übernehmen
if len(sys.argv) < 2:
    raise ValueError("Bitte gib die MongoDB-Verbindungszeichenfolge als Argument mit -u an.")

CONNECTION_STRING = sys.argv[1]
client = MongoClient(CONNECTION_STRING)

db = client["energiedaten"]
collection = db["stromdaten"]

df = pd.read_csv("data/processed/stromdaten.csv")
