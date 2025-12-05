# pip install pyarrow

import pandas as pd
from flask import *
from collections import Counter
import plotly 
from plotly import *
import matplotlib.pyplot as plt
from matplotlib import *
import requests


app = Flask(__name__)

#call in raw data once
full_data = pd.read_parquet(r"C:\Users\carol\compmethods-cg2288\final_project\clean_data.parquet")

#bring in images
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

# helper function pulling state and county counts
def state_county_counts(state_name):
    r = (requests.get(f"http://127.0.0.1:5002/api/county-codes?state={state_name}", headers={"User-Agent": "MyScript"}))
    return r.json()

# helper function for analysis 
def compute_did(df1_group, df2_group, category):
    """
    Computes the Difference-in-Differences given two grouped dataframes:
    df1_group: RUCC 1 group (YEAR + category)
    df2_group: RUCC 2 group (YEAR + category)
    """
    # Ensure sorted by YEAR
    df1_group = df1_group.sort_values("YEAR")
    df2_group = df2_group.sort_values("YEAR")

    # Extract first and last year
    year_start = df1_group["YEAR"].iloc[0]
    year_end = df1_group["YEAR"].iloc[-1]

    # Get means for each year and category
    g1_start = df1_group[df1_group["YEAR"] == year_start][category].values[0]
    g1_end = df1_group[df1_group["YEAR"] == year_end][category].values[0]
    g2_start = df2_group[df2_group["YEAR"] == year_start][category].values[0]
    g2_end = df2_group[df2_group["YEAR"] == year_end][category].values[0]

    # Compute changes
    change_g1 = g1_end - g1_start
    change_g2 = g2_end - g2_start

    # Difference-in-differences
    did = change_g1 - change_g2

    return {
        "year_start": year_start,
        "year_end": year_end,
        "g1_start": g1_start,
        "g1_end": g1_end,
        "g2_start": g2_start,
        "g2_end": g2_end,
        "change_g1": change_g1,
        "change_g2": change_g2,
        "did": did,
    }


# landing page
@app.route("/home")
def home():
    return render_template("home_gheen.html")

# redirect to home
@app.route('/')
def root():
    return redirect("/home")

# index page
@app.route("/index")
def index():
    return render_template("index_gheen.html")

# analyze page and add images
@app.route("/analyze", methods=["POST"])
def analyze():
    usertext = request.form["usertext"]
    counts = state_county_counts(usertext)
    analyze_text = ""
    state_image = usertext.lower().replace(" ", "_") + ".png"
    return render_template("analyze_gheen.html", analysis=analyze_text, usertext=usertext, state_image=state_image, counts=counts)

# about the dataset page
@app.route("/dataset", methods=["GET", "POST"])
def dataset():
    return render_template("dataset_gheen.html")

#input what to compare
@app.route("/compare", methods=["GET", "POST"])
def graphs():
    print(request.form)
    category = request.form.get("category")
    rucc1 = request.form.get("rucc1")
    rucc2 = request.form.get("rucc2")
    region1 = request.form.get("region1")
    region2 = request.form.get("region2")

    human_readable = {"POS_MAX_DIST_ED": "Maximum Distance to ER", 
        "POS_MEAN_DIST_ED": "Mean Distance to ER",
        "POS_MEDIAN_DIST_ED": "Median Distance to ER",
        "POS_MAX_DIST_TRAUMA": "Maximum Distance to Trauma Center",
        "POS_MEAN_DIST_TRAUMA": "Mean Distance to Trauma Center",
        "POS_MEDIAN_DIST_TRAUMA": "Median Distance to Trauma Center",
        "POS_MAX_DIST_MEDSURG_ICU": "Maximum Distance to ICU",
        "POS_MEAN_DIST_MEDSURG_ICU": "Mean Distance to ICU",
        "POS_MEDIAN_DIST_MEDSURG_ICU": "Median Distance to ICU",
        "POS_ASC_RATE":"Total Number of Ambulatory Surgery Centers"}

    category = request.form.get("category") or request.args.get("category")

    category_readable = human_readable.get(category, "Unknown Category") # convert to human-readable
    return render_template("deeper_analysis_gheen.html", category_readable=category_readable, category=category, rucc1=rucc1, rucc2=rucc2, region1=region1, region2=region2)

#show graphs 
@app.route("/graphs", methods=["POST"])
def deep_analyze():
    print(request.form)
    category = request.form["category"]
    rucc1 = int(request.form["rucc1"])
    rucc2 = int(request.form["rucc2"])
    region1 = request.form.get("region1")
    region2 = request.form.get("region2")

    df1 = full_data[full_data['AHRF_USDA_RUCC_2013'] == rucc1]
    df2 = full_data[full_data['AHRF_USDA_RUCC_2013'] == rucc2]

    # -------- RUCC 1 ----------
    if region1 == "All":
        df1_group = df1.groupby('YEAR')[category].mean().reset_index()
    else:
        df1_group = df1[df1["REGION"] == region1].groupby('YEAR')[category].mean().reset_index()

    # -------- RUCC 2 ----------
    if region2 == "All":
        df2_group = df2.groupby('YEAR')[category].mean().reset_index()
    else:
        df2_group = df2[df2["REGION"] == region2].groupby('YEAR')[category].mean().reset_index()

    # 🔥 ADDED: compute Difference-in-Differences
    did_results = compute_did(df1_group, df2_group, category)

    # Plotly-ready data
    plot_data = [
        {
            "x": df1_group["YEAR"].tolist(),
            "y": df1_group[category].tolist(),
            "mode": "lines+markers",
            "name": f"RUCC {rucc1} in {region1}",
        },
        {
            "x": df2_group["YEAR"].tolist(),
            "y": df2_group[category].tolist(),
            "mode": "lines+markers",
            "name": f"RUCC {rucc2} in {region2}",
        },
    ]

    layout = {
        "xaxis": {"title": "Year"},
        "yaxis": {"title": "Distance in Miles"},
        "hovermode": "x unified",
    }

    human_readable = {"POS_MAX_DIST_ED": "Maximum Distance to ER", 
        "POS_MEAN_DIST_ED": "Mean Distance to ER",
        "POS_MEDIAN_DIST_ED": "Median Distance to ER",
        "POS_MAX_DIST_TRAUMA": "Maximum Distance to Trauma Center",
        "POS_MEAN_DIST_TRAUMA": "Mean Distance to Trauma Center",
        "POS_MEDIAN_DIST_TRAUMA": "Median Distance to Trauma Center",
        "POS_MAX_DIST_MEDSURG_ICU": "Maximum Distance to ICU",
        "POS_MEAN_DIST_MEDSURG_ICU": "Mean Distance to ICU",
        "POS_MEDIAN_DIST_MEDSURG_ICU": "Median Distance to ICU",
        "POS_ASC_RATE":"Total Number of Ambulatory Surgery Centers"}

    category_readable = human_readable.get(category, category)

    return render_template(
        'compare_graphs_gheen.html',
        plot_data=plot_data,
        plot_layout=layout,
        category=category,
        category_readable=category_readable,
        rucc1=rucc1,
        rucc2=rucc2,
        region1=region1,
        region2=region2,
        did_results=did_results,  # 🔥 PASS RESULTS TO TEMPLATE
    )

#API call for RUCC breakdown
@app.route("/api/county-codes", methods=["GET"])
def api_county_codes():
    state = request.args.get("state")
    if not state:
        return jsonify({'error':'Missing ?state= parameter'}), 400
    state_data = full_data[full_data['STATE'].str.lower() == state.lower()]
    state_data = state_data[state_data['YEAR'] == 2013]
    state_data = state_data.fillna(0)
    county_category_counts = state_data['AHRF_USDA_RUCC_2013'].astype(int).value_counts().sort_index().to_dict()
    return jsonify({
        'state': state,
        'county_category_counts': county_category_counts
    })


if __name__ == "__main__":
    app.run(debug=True, port=5002)

