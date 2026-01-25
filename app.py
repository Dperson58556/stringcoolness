import functions_imports as fi
from flask import Flask, jsonify, request, render_template

# APPLICATION SETUP
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate")
def generate():
    length = int(request.args.get("length", 8))
    rolls = int(request.args.get("rolls", 1))

    results = [fi.generate_scored_string(length) for _ in range(rolls)]

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

