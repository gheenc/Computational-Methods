# pip install pyarrow

import pandas as pd
from flask import *
from collections import Counter
import plotly 
from plotly import *
import matplotlib.pyplot as plt
from matplotlib import *


app = Flask(__name__)

#call in raw data once
full_data = pd.read_parquet(r"C:\Users\carol\compmethods-cg2288\final_project\clean_data.parquet")

#bring in images
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

# helper function pulling state and county counts
def state_county_counts(state_name, year=2013):
    state_data = full_data[full_data['STATE'].str.lower() == state_name.lower()]
    state_data = state_data[state_data['YEAR'] == year]
    state_data = state_data.fillna(0)
    county_counts = state_data['AHRF_USDA_RUCC_2013'].astype(int).value_counts().sort_index().to_dict()
    return county_counts 

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

# analyze page
@app.route("/analyze", methods=["POST"])
def analyze():
    usertext = request.form["usertext"]
    counts = state_county_counts(usertext)
    analyze_text = ""
    for category, count in counts.items():
        analyze_text += f"Category {category}: {count}\n "
    state_image = usertext.lower().replace(" ", "_") + "_code.png"
    return render_template("analyze_gheen.html", analysis=analyze_text, usertext=usertext, state_image=state_image)

# about the dataset page
@app.route("/dataset", methods=["GET", "POST"])
def dataset():
    return render_template("dataset_gheen.html")

# shows deeper analysis/graphs page to input 
@app.route("/compare", methods=["GET", "POST"])
def graphs():
    category = request.form.get("category")
    rucc1 = request.form.get("rucc1")
    rucc2 = request.form.get("rucc2")

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

    category_readable = human_readable.get(category, "Unknown Category") # convert to human-readable
    return render_template("deeper_analysis_gheen.html", category_readable=category_readable, category=category, rucc1=rucc1, rucc2=rucc2)


#deeper analysis page of graphs
@app.route("/graphs", methods=["POST"])
def deep_analyze():
    category = request.form["category"]
    rucc1 = int(request.form["rucc1"])
    rucc2 = int(request.form["rucc2"]) # defined/pulled from deeper analysis page

    df1 = full_data[full_data['AHRF_USDA_RUCC_2013'] == rucc1]
    df2 = full_data[full_data['AHRF_USDA_RUCC_2013'] == rucc2] # pulls ruccs wanted 

    df1_group = df1.groupby('YEAR')[category].mean().reset_index() # groups each year and get mean for graphing 
    df2_group = df2.groupby('YEAR')[category].mean().reset_index()

    print(df1_group)
    print(df2_group)

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

    # Plotly-ready data
    plot_data = [
        {
            "x": df1_group["YEAR"].tolist(),
            "y": df1_group[category].tolist(),
            "mode": "lines+markers",
            "name": f"RUCC {rucc1}",
        },
        {
            "x": df2_group["YEAR"].tolist(),
            "y": df2_group[category].tolist(),
            "mode": "lines+markers",
            "name": f"RUCC {rucc2}",
        },
    ]

    layout = {
        "xaxis": {"title": "Year"},
        "yaxis": {"title": "Distance in Miles"},
        "hovermode": "x unified",
    }

    category_readable = human_readable.get(category, category)

    return render_template('compare_graphs_gheen.html', plot_data=plot_data, plot_layout=layout, category=category, rucc1=rucc1, rucc2=rucc2, graph=graphs, category_readable=category_readable)

# shows page for starting k-nearest neighbors clustering
@app.route("/clustering", methods=["GET", "POST"])
def clusters():
    return render_template("clustering_gheen.html")

# page showing results of clustering 
@app.route("/clusters", methods=["GET", "POST"])
def clustering():
    return render_template("clustering_results_gheen.html")

#API call for RUCC breakdown
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

