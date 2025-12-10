# pip install pyarrow

import pandas as pd
from flask import *
from collections import Counter
import plotly 
from plotly import *
import matplotlib.pyplot as plt
from matplotlib import *
import requests
import statsmodels.api as sm
import statsmodels.formula.api as smf



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

# helper function for anova
def run_two_way_anova(df1, df2, category):
    # Add RUCC labels so the model knows which group each row is in
    df1 = df1.copy()
    df2 = df2.copy()
    df1["RUCC_GROUP"] = "Group1"
    df2["RUCC_GROUP"] = "Group2"

    # Combine into one dataframe
    df = pd.concat([df1, df2], ignore_index=True)

    # Convert categorical variables
    df["YEAR"] = df["YEAR"].astype(int).astype("category")
    df["RUCC_GROUP"] = df["RUCC_GROUP"].astype("category")

    # Build the two-way ANOVA model with interaction
    formula = f"{category} ~ YEAR * RUCC_GROUP"
    model = smf.ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)  # Type II ANOVA

    return model, anova_table

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
    show_image = usertext != "District of Columbia"
    state_image = usertext.lower().replace(" ", "_") + ".png" if show_image else None
    legend = "legend.png" if show_image else None
    return render_template("analyze_gheen.html", analysis=analyze_text, usertext=usertext, state_image=state_image, counts=counts, legend=legend, show_image=show_image)

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

    model, anova_table = run_two_way_anova(df1, df2, category)
    
    # Extract p-values
    p_year = anova_table.loc["YEAR", "PR(>F)"]
    p_rucc = anova_table.loc["RUCC_GROUP", "PR(>F)"]
    p_interaction = anova_table.loc["YEAR:RUCC_GROUP", "PR(>F)"]

    # Interpret the interaction (Difference-in-Differences)
    if p_interaction < 0.05:
        did_interpretation = "The change over time is significantly different between the two RUCC groups."
    else:
        did_interpretation = "No significant difference in change over time between the two RUCC groups."

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
    rucc1=rucc1,
    rucc2=rucc2,
    graph=graphs,
    category_readable=category_readable,
    region1=region1,
    region2=region2,
    anova_table=anova_table.to_html(classes="table table-striped"),
    p_year=p_year,
    p_rucc=p_rucc,
    p_interaction=p_interaction)


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

