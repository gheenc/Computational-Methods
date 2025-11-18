# css style from: https://www.w3schools.com/Css/tryit.asp?filename=trycss_default

import pandas as pd
from flask import Flask, render_template, request, jsonify 
from collections import Counter

app = Flask(__name__)

# helper function pulling state and county counts
def state_county_counts(state_name):
    data = pd.read_excel('data/SDOH_2020_COUNTY_Cleaned.xlsx', sheet_name='Data')
    state_data = data[data['STATE'].str.lower() == state_name.lower()]
    county_counts = state_data['AHRF_USDA_RUCC_2013'].astype(int).value_counts().sort_index().to_dict()
    return county_counts 


# index page
@app.route("/")
def index():
    return render_template("index_gheen.html")

# analyze page
@app.route("/analyze", methods=["POST"])
def analyze():
    usertext = request.form["usertext"]
    counts = state_county_counts(usertext)
    analyze_text = ""
    for category, count in counts.items():
        analyze_text += f"Category {category}: {count}\n "
    return render_template("analyze_gheen.html", analysis=analyze_text, usertext=usertext)

@app.route("/api/county-codes", methods=["GET"])
def api_county_codes():
    state = request.args.get("state")
    if not state:
        return jsonify({'error':'Missing ?state= parameter'}), 400
    counts = state_county_counts(state)
    return jsonify({
        'state': state,
        'county_category_counts': counts
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)

