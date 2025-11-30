import pandas as pd
from flask import *
from collections import Counter
import plotly 
from plotly import *

app = Flask(__name__)

#bring in images
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

# helper function pulling state and county counts
def state_county_counts(state_name):
    data = pd.read_excel('data/SDOH_2020_COUNTY_Cleaned.xlsx', sheet_name='Data')
    state_data = data[data['STATE'].str.lower() == state_name.lower()]
    state_data = state_data.fillna(0)
    county_counts = state_data['AHRF_USDA_RUCC_2013'].astype(int).value_counts().sort_index().to_dict()
    return county_counts 

#helper function to do analysis - total er 2020 
def counts_total_ER_2020():
    data = pd.read_excel('data/COMBINED CLEAN.xlsx', sheet_name='2020')
    data = data.drop(data.index[0])
    data = data.fillna("NA")
    counts = data["RUCC_CODE"].value_counts().sort_index().reset_index()
    counts.columns = ["RUCC_CODE", "County_Count"]
    average_ER_counts = (data.groupby("RUCC_CODE", as_index=False)["TOTAL_ER"].mean())
    average_ER_counts.columns = ["RUCC_CODE", "Avg_ER"]
    final_df = counts.merge(average_ER_counts, on="RUCC_CODE", how="left") #
    return final_df
    #fig = px.bar(final_df, x=[1, 2, 3, 4, 5, 6, 7, 8, 9], y="Avg_ER",
                 #title = "Average Amounts of Hospitals with ER per County Classification in US",
                 #labels={"RUCC_CODE": "Rural-Metro Code", "Avg_ER": "Average Number of ERs"},
                #text=final_df["Avg_ER"].round(2).astype(str))
    #fig.savefig("static/plot_age_er.png", bbox_inces="tight")


#helper function analysis - total er 2020 rate
def counts_total_ER_rate_2020():
    data = pd.read_excel('data/COMBINED CLEAN.xlsx', sheet_name='2020')
    data = data.drop(data.index[0])
    data = data.fillna("NA")
    counts = data["RUCC_CODE"].value_counts().sort_index()
    counts.columns = ["RUCC_CODE", "County_Count"]
    average_ER_rate_counts = (data.groupby("RUCC_CODE", as_index=False)["TOTAL_ER_RATE"].mean())
    average_ER_rate_counts.columns = ["RUCC_CODE", "Avg_ER_Rate"]
    final_df = counts.merge(average_ER_rate_counts, on="RUCC_CODE", how="left")
    return final_df

#helpful function for selecting region and 2 classifications to compare 



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

# deeper analysis/graphs page
@app.route("/graphs", methods=["GET", "POST"])
def graphs():
    counts_total_ER_2020()
    counts_total_ER_2020()
    return render_template("deeper_analysis_gheen.html")

#API call
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

