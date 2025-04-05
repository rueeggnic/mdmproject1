import pandas as pd

# CSV-Dateien laden (Datum-Spalten anpassen falls nötig)
df_speicherseen = pd.read_csv('data/processed/fuellstand_speicherseen.csv', parse_dates=['Datum'])
df_stromdaten = pd.read_csv('data/processed/stromdaten.csv', parse_dates=['date'])

# Sortieren nach Datum (wichtig für Suche des letzten gültigen Wertes)
df_speicherseen.sort_values('Datum', inplace=True)
df_stromdaten.sort_values('date', inplace=True)

# Start- und Enddatum definieren
start_datum = pd.to_datetime('2014-01-06')
end_datum = df_stromdaten['date'].max()

# Ergebnisse speichern
ergebnisse = []

aktuelles_datum = start_datum

# For-loop über alle Tage
while aktuelles_datum <= end_datum:
    # Täglichen Stromdaten-Wert holen
    strom_werte = df_stromdaten.loc[df_stromdaten['date'] == aktuelles_datum, df_stromdaten.columns[5]].values
    if strom_werte.size == 0:
        print(f"Kein Stromdaten-Wert am {aktuelles_datum.date()}, überspringe diesen Tag.")
        aktuelles_datum += pd.Timedelta(days=1)
        continue  # Überspringen, falls kein Strom-Wert vorhanden ist
    wert_strom = float(strom_werte[0])

    # Letzten gültigen Wert von Speicherseen holen
    df_vorher = df_speicherseen[df_speicherseen['Datum'] <= aktuelles_datum]
    df_woche_vorher = df_speicherseen[df_speicherseen['Datum'] <= (aktuelles_datum - pd.Timedelta(days=7))]

    if df_vorher.empty or df_woche_vorher.empty:
        print(f"Unzureichende Speicherseen-Daten am {aktuelles_datum.date()}, überspringe diesen Tag.")
        aktuelles_datum += pd.Timedelta(days=1)
        continue

    wert_speicher = float(df_vorher.iloc[-1, 5])
    wert_speicher_vorwoche = float(df_woche_vorher.iloc[-1, 5])

    # Neue Berechnung durchführen
    ergebnis = (wert_speicher - wert_speicher_vorwoche) / 7 + wert_strom

    # Ergebnis speichern
    ergebnisse.append({
        'Datum': aktuelles_datum.date(),
        'Datum_Speicherseen': df_vorher.iloc[-1]['Datum'].date(),
        'Pot_Energie_Stauseen_gwh': wert_speicher,
        'erzeugte_Energie_Speicherkraft_gwh': wert_strom,
        'Zufluss_Stauseen_gwh': ergebnis
    })

    aktuelles_datum += pd.Timedelta(days=1)

# Ergebnisse als DataFrame speichern und in CSV exportieren
df_ergebnisse = pd.DataFrame(ergebnisse)
df_ergebnisse.to_csv('data/processed/zuflussmenge.csv', index=False)

print("Berechnung abgeschlossen. Ergebnisse in 'zuflussmenge.csv' gespeichert.")
