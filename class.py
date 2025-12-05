from flask import * 

my_template = """
<html>

<head>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script>
        // data from https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
        // accessed 12-4-2025
        let data = [{
            "locations": ["AL", "AK", "AZ", "AR", "CA", "CO", "CT"], /*pull from the dataset*/
            "z": [20.9, 21, 15.6, 22.3, 11.3, 14.6, 12.7], */pull from dataset*/
            "locationmode": "USA-states",
            "type": "choropleth"
        }];
        let layout = {
            "title": "Smoking rates by state (%)",
            "geo": {
                "scope": "usa"
            }
        };
        $(() => {
            // everything here happens only after the page is loaded
            Plotly.newPlot("myGraph", data, layout);
        });
    </script>
    <style>
        #myGraph {
            width: 600px;
            height: 400px
        }
    </style>
</head>

<body>
    <div>Here is our graph:</div>
    <div id="myGraph"></div>
</body>

</html>
"""

app = Flask(__name__)

@app.route("/")
def home():
    states = {"Alabama":}
    return my_template

if __name__ == "__main__":
    app.run(debug=True)


#code API
# https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv