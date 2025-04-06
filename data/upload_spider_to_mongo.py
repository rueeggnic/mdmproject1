import json
import pymongo
import os

# MongoDB-Verbindungs-URI aus Secret (z. B. von GitHub oder lokal gesetzt)
MONGO_URI = os.environ.get("MONGODB_URI1")

if not MONGO_URI:
    raise ValueError("Umgebungsvariable MONGODB_URI1 ist nicht gesetzt!")

# Verbindung zur MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client["demo_scraping"]          # <--- eigene, saubere Demo-DB
collection = db["hikrgpx_spider"]     # <--- eigene Demo-Collection

# Lade Scrapy-Daten
input_file = "data/gpx_output.jl"

print(f"📂 Lade Daten aus: {input_file}")
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        doc = json.loads(line)
        collection.insert_one(doc)

print(f"✅ Import abgeschlossen: {collection.count_documents({})} Dokumente in 'demo_scraping.hikrgpx_spider'")
