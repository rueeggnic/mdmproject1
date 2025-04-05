import requests
import pandas as pd

url = "https://www.energiedashboard.admin.ch/api/strom/strom-produktion-import-verbrauch"

response = requests.get(url)
data = response.json()

# Wichtig: Extrahiere explizit die Daten aus "entries":
df = pd.json_normalize(data["entries"])

print(df.head())

# Optional: CSV-Datei speichern
df.to_csv("data/processed/stromdaten.csv", index=False)
