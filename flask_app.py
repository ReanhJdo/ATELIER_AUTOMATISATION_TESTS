import json
from flask import Flask, jsonify, render_template, redirect, url_for
from tester.runner import run_all_tests
from storage import save_run, list_runs

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("dashboard"))

@app.route("/run", methods=["GET", "POST"])
def trigger_run():
    data = run_all_tests()
    save_run(data)
    return redirect(url_for("dashboard"))

@app.route("/api/run", methods=["GET", "POST"])
def api_run():
    data = run_all_tests()
    save_run(data)
    return jsonify(data)

@app.route("/dashboard")
def dashboard():
    runs = list_runs(limit=15)
    last_run = json.loads(runs[0]["payload"]) if runs else None
    return render_template("dashboard.html", runs=runs, last_run=last_run)

@app.route("/health")
def health():
    runs = list_runs(limit=1)
    if not runs:
        return jsonify({"status": "UNKNOWN", "message": "Aucun run exécuté"}), 200
    
    last = runs[0]
    status = "UP" if last["failed"] == 0 else "DEGRADED"
    return jsonify({
        "status": status,
        "last_timestamp": last["timestamp"],
        "error_rate": last["error_rate"],
        "latency_avg_ms": last["latency_avg"]
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
