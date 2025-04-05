# Basis-Image mit Python
FROM python:3.12

# Arbeitsverzeichnis im Container
WORKDIR /usr/src/app

# Projektdateien kopieren (alles unter data/)
COPY data ./data

# Falls requirements.txt vorhanden – bitte anpassen, falls Pfad anders ist
COPY requirements.txt .

# Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Port für Flask (Standard: 5000)
EXPOSE 5000

# Flask starten
ENV FLASK_APP=data/models/app.py
CMD ["flask", "run", "--host=0.0.0.0"]
