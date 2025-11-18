# css style from: https://www.w3schools.com/Css/tryit.asp?filename=trycss_default


from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index_gheen.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    usertext = request.form["usertext"]
    counts = Counter(usertext)
    result = ""
    for item, count in counts.items():
        result += f"The character '{item}' appears {count} times.\n"
    return render_template("analyze.html", analysis=result, usertext=usertext)


if __name__ == "__main__":
    app.run(debug=True, port=5002)