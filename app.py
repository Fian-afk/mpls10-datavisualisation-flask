"""Dashboard statistik hero MPL Indonesia Season 10."""
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template

app = Flask(__name__)

DATA_PATH = Path(__file__).resolve().parent / "data" / "MPL_ID_S10.csv"
COUNT_COLUMNS = ["Hero_picked", "T_wins", "T_lose", "Hero_banned", "Pick&Ban"]
df = pd.read_csv(DATA_PATH)

required_columns = {"Hero", *COUNT_COLUMNS}
missing_columns = required_columns.difference(df.columns)
if missing_columns:
    raise ValueError(f"Kolom wajib tidak ditemukan di {DATA_PATH}: {sorted(missing_columns)}")

for column in COUNT_COLUMNS:
    df[column] = pd.to_numeric(df[column], errors="raise")


def persentase(menang, total):
    """Hitung persentase, atau None jika belum ada pertandingan."""
    if total == 0:
        return None
    return round(float(menang / total * 100), 1)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/ringkasan")
def ringkasan():
    total_picks = int(df["Hero_picked"].sum())
    return jsonify(
        jumlah_hero=int(df["Hero"].nunique()),
        total_pick=total_picks,
        total_ban=int(df["Hero_banned"].sum()),
        win_rate=persentase(df["T_wins"].sum(), total_picks),
        hero_terpopuler=df.loc[df["Pick&Ban"].idxmax(), "Hero"],
    )


@app.route("/api/statistik-hero")
def statistik_hero():
    top_pick = df.nlargest(10, "Hero_picked")
    top_ban = df.nlargest(10, "Hero_banned")
    hero_dengan_cukup_pick = df[df["Hero_picked"] >= 10].copy()
    hero_dengan_cukup_pick["win_rate"] = (
        hero_dengan_cukup_pick["T_wins"] / hero_dengan_cukup_pick["Hero_picked"] * 100
    )
    top_win_rate = hero_dengan_cukup_pick.nlargest(10, "win_rate")

    return jsonify(
        top_pick={
            "labels": top_pick["Hero"].tolist(),
            "data": top_pick["Hero_picked"].astype(int).tolist(),
        },
        top_ban={
            "labels": top_ban["Hero"].tolist(),
            "data": top_ban["Hero_banned"].astype(int).tolist(),
        },
        top_win_rate={
            "labels": top_win_rate["Hero"].tolist(),
            "data": top_win_rate["win_rate"].round(1).tolist(),
            "jumlah_pick": top_win_rate["Hero_picked"].astype(int).tolist(),
        },
    )


if __name__ == "__main__":
    app.run(debug=True)
