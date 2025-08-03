from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
CSV_PATH = "data/controls.csv"

if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(CSV_PATH):
    df_init = pd.DataFrame([
        ["LOG-01", "Audit Logging Enabled", "Das System muss sicherstellen, dass Audit-Logging für sicherheitsrelevante Ereignisse aktiv ist", "offen", "", ""],
        ["LOG-02", "Log Storage and Protection", "Logs müssen vor unbefugtem Zugriff und Veränderung geschützt gespeichert werden", "offen", "", ""]
    ], columns=["ID", "Kontrolle", "Beschreibung", "Status", "Kommentar", "Nachweis-Link"])
    df_init.to_csv(CSV_PATH, index=False)

@app.route("/", methods=["GET", "POST", "HEAD"])
def index():
    if request.method == "HEAD":
        return "", 200
    df = pd.read_csv(CSV_PATH)
    if request.method == "POST":
        idx = int(request.form["row"])
        df.at[idx, "Status"] = request.form["status"]
        df.at[idx, "Kommentar"] = request.form.get("kommentar", "")
        df.at[idx, "Nachweis-Link"] = request.form.get("nachweis", "")
        df.to_csv(CSV_PATH, index=False)
    return render_template("index.html", data=df.to_dict(orient="records"))

@app.route("/export")
def export():
    df = pd.read_csv(CSV_PATH)
    out_file = "cloud_audit_export.xlsx"
    df.to_excel(out_file, index=False)
    return send_file(out_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
