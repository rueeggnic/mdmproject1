# model_prediction.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_simulation(pv_faktor=1, wind_faktor=1, kernkraft_faktor=1):
    df_zufluss = pd.read_csv("data/processed/zuflussmenge.csv", parse_dates=["date"])
    df_strom = pd.read_csv("data/processed/stromdaten.csv", parse_dates=["date"])

    df_strom.fillna({"photovoltaik": 0, "wind": 0}, inplace=True)
    df = df_strom.merge(df_zufluss, on="date")
    df.set_index("date", inplace=True)

    initial_fuellstand = df["fuellstand_gwh"].iloc[0]
    simulation_df = df.copy()

    simulation_df["stromverbrauch"] = df["stromverbrauch"]
    simulation_df["nettoimporte"] = df["nettoimporte"]

    simulation_df["photovoltaik"] = df["photovoltaik"] * pv_faktor
    simulation_df["wind"] = df["wind"] * wind_faktor
    simulation_df["kernkraft"] = df["kernkraft"] * kernkraft_faktor

    simulation_df["flusskraft"] = df["flusskraft"]
    simulation_df["thermische"] = df["thermische"]
    simulation_df["zufluss_gwh"] = df["zufluss_gwh"]

    simulation_df["fuellstand_gwh_simuliert"] = np.nan
    simulation_df["speicherkraft_simuliert"] = np.nan

    fuellstand = initial_fuellstand
    simulation_df.sort_index(inplace=True)

    erster_tag = simulation_df.index[0]
    verbrauch_erster_tag = simulation_df.at[erster_tag, "stromverbrauch"]
    nettoimporte_erster_tag = simulation_df.at[erster_tag, "nettoimporte"]

    produktion_ohne_speicher_erster_tag = (
        simulation_df.at[erster_tag, "kernkraft"] +
        simulation_df.at[erster_tag, "thermische"] +
        simulation_df.at[erster_tag, "flusskraft"] +
        simulation_df.at[erster_tag, "wind"] +
        simulation_df.at[erster_tag, "photovoltaik"] +
        nettoimporte_erster_tag
    )

    speicherkraft_erster_tag = max(verbrauch_erster_tag - produktion_ohne_speicher_erster_tag, 0)
    fuellstand = max(min(fuellstand + simulation_df.at[erster_tag, "zufluss_gwh"] - speicherkraft_erster_tag, df["fuellstand_gwh"].max()), 0)

    simulation_df.at[erster_tag, "speicherkraft_simuliert"] = speicherkraft_erster_tag
    simulation_df.at[erster_tag, "fuellstand_gwh_simuliert"] = fuellstand

    for tag in simulation_df.index[1:]:
        verbrauch = simulation_df.at[tag, "stromverbrauch"]
        nettoimporte = simulation_df.at[tag, "nettoimporte"]

        produktion_ohne_speicher = (
            simulation_df.at[tag, "kernkraft"] +
            simulation_df.at[tag, "thermische"] +
            simulation_df.at[tag, "flusskraft"] +
            simulation_df.at[tag, "wind"] +
            simulation_df.at[tag, "photovoltaik"] +
            nettoimporte
        )

        speicherkraft = max(verbrauch - produktion_ohne_speicher, 0)
        fuellstand = fuellstand + simulation_df.at[tag, "zufluss_gwh"] - speicherkraft
        fuellstand = max(min(fuellstand, df["fuellstand_gwh"].max()), 0)

        simulation_df.at[tag, "speicherkraft_simuliert"] = speicherkraft
        simulation_df.at[tag, "fuellstand_gwh_simuliert"] = fuellstand

    return simulation_df

if __name__ == "__main__":
    result = run_simulation()
    print(result.tail())