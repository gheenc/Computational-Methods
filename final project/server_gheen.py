# css style from: https://www.w3schools.com/Css/tryit.asp?filename=trycss_default

import pandas as pd
from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index_gheen.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    usertext = request.form["usertext"]
    df = pd.read_excel('data/SDOH_2020_COUNTY_Cleaned.xlsx', sheet_name='Data')
    state_data = df[df['STATE'].str.lower() == usertext.lower()]
    county_counts = state_data['AHRF_USDA_RUCC_2013'].astype(int).value_counts().sort_index()
    result = ""
    for category, count in county_counts.items():
        result += f"Category {category}: {count}\n "
    return render_template("analyze_gheen.html", analysis=result, usertext=usertext)


if __name__ == "__main__":
    app.run(debug=True, port=5002)