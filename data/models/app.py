# app.py
from flask import Flask, request, jsonify, send_file, render_template_string
import matplotlib.pyplot as plt
import io
import base64
from model_prediction import run_simulation

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Simulation starten</title>
</head>
<body>
    <h2>Energiemodell Simulation</h2>
    <form method="get" action="/">
        <label>PV-Faktor: <input type="number" step="0.1" name="pv" value="{{ pv }}"></label><br><br>
        <label>Wind-Faktor: <input type="number" step="0.1" name="wind" value="{{ wind }}"></label><br><br>
        <label>Kernkraft-Faktor: <input type="number" step="0.1" name="kern" value="{{ kern }}"></label><br><br>
        <input type="submit" value="Simulation starten">
    </form>
    {% if image %}
    <h3>Simulationsergebnis</h3>
    <img src="data:image/png;base64,{{ image }}" />
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    pv = float(request.args.get("pv", 1))
    wind = float(request.args.get("wind", 1))
    kern = float(request.args.get("kern", 1))

    image_data = None
    if "pv" in request.args:
        df = run_simulation(pv, wind, kern)

        fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        df["fuellstand_gwh_simuliert"].plot(ax=ax[0], label="Simuliert", color="blue")
        df["fuellstand_gwh"].plot(ax=ax[0], label="Historisch", linestyle='--', color="grey")
        ax[0].legend()
        ax[0].set_title("Füllstand")

        df["speicherkraft_simuliert"].plot(ax=ax[1], label="Simuliert", color="green")
        df["speicherkraft"].plot(ax=ax[1], label="Historisch", linestyle='--', color="grey")
        ax[1].legend()
        ax[1].set_title("Speicherkraft")

        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plt.close()

        image_data = base64.b64encode(img.read()).decode("utf-8")

    return render_template_string(HTML_FORM, pv=pv, wind=wind, kern=kern, image=image_data)

@app.route("/simulate")
def simulate():
    pv = float(request.args.get("pv", 1))
    wind = float(request.args.get("wind", 1))
    kern = float(request.args.get("kern", 1))

    df = run_simulation(pv, wind, kern)

    last = df.iloc[-1][["fuellstand_gwh_simuliert", "speicherkraft_simuliert"]].to_dict()
    return jsonify(last)

if __name__ == "__main__":
    app.run(debug=True)