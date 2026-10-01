from flask import Flask, jsonify, render_template_string
import json
import os

app = Flask(__name__)

DATA_FILE = "dashboard_data.json"

DEFAULT_DATA = {
    "mq135": 0,
    "mq3": 0,
    "mq4": 0,
    "score": 0,
    "result": "WAITING FOR TEST",
    "readings": 0,
    "timestamp": "--"
}


def get_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass

    return DEFAULT_DATA


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MHE Breath Analysis</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0b1020;
            color: white;
        }

        .header {
            padding: 25px;
            text-align: center;
            background: #111827;
            border-bottom: 1px solid #263043;
        }

        .header h1 {
            margin: 0;
            font-size: 28px;
        }

        .header p {
            color: #9ca3af;
        }

        .container {
            max-width: 1100px;
            margin: auto;
            padding: 25px;
        }

        .result {
            padding: 30px;
            border-radius: 18px;
            text-align: center;
            margin-bottom: 25px;
            background: #182235;
            border: 1px solid #334155;
        }

        .result h2 {
            font-size: 32px;
            margin: 10px;
        }

        .score {
            font-size: 20px;
            color: #cbd5e1;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .card {
            background: #182235;
            padding: 25px;
            border-radius: 18px;
            border: 1px solid #334155;
            text-align: center;
        }

        .card h3 {
            color: #94a3b8;
            margin-bottom: 10px;
        }

        .value {
            font-size: 36px;
            font-weight: bold;
        }

        .info {
            margin-top: 25px;
            background: #182235;
            padding: 25px;
            border-radius: 18px;
            border: 1px solid #334155;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #263043;
        }

        .warning {
            margin-top: 25px;
            padding: 15px;
            border-radius: 10px;
            background: #332b16;
            color: #facc15;
            text-align: center;
        }

        @media(max-width: 700px) {
            .cards {
                grid-template-columns: 1fr;
            }
        }
    </style>

    <script>
        async function updateDashboard() {
            const response = await fetch('/api/data');
            const data = await response.json();

            document.getElementById("result").innerText = data.result;

            document.getElementById("score").innerText =
                data.score.toFixed(1) + "%";

            document.getElementById("mq135").innerText =
                data.mq135.toFixed(2);

            document.getElementById("mq3").innerText =
                data.mq3.toFixed(2);

            document.getElementById("mq4").innerText =
                data.mq4.toFixed(2);

            document.getElementById("readings").innerText =
                data.readings;

            document.getElementById("timestamp").innerText =
                data.timestamp;
        }

        setInterval(updateDashboard, 2000);

        window.onload = updateDashboard;
    </script>

</head>

<body>

<div class="header">
    <h1>🫁 MHE Breath Analysis System</h1>
    <p>ESP32 + MQ135 + MQ3 + MQ4</p>
</div>

<div class="container">

    <div class="result">

        <p>SCREENING RESULT</p>

        <h2 id="result">
            WAITING FOR TEST
        </h2>

        <div class="score">
            Demo Score:
            <strong id="score">0%</strong>
        </div>

    </div>

    <div class="cards">

        <div class="card">
            <h3>MQ135</h3>
            <div class="value" id="mq135">0</div>
        </div>

        <div class="card">
            <h3>MQ3</h3>
            <div class="value" id="mq3">0</div>
        </div>

        <div class="card">
            <h3>MQ4</h3>
            <div class="value" id="mq4">0</div>
        </div>

    </div>

    <div class="info">

        <h2>Test Information</h2>

        <div class="info-row">
            <span>Readings collected</span>
            <strong id="readings">0</strong>
        </div>

        <div class="info-row">
            <span>Last update</span>
            <strong id="timestamp">--</strong>
        </div>

    </div>

    <div class="warning">

        ⚠️ Experimental SIH prototype.
        The current model uses synthetic demonstration data
        and is not clinically validated.

    </div>

</div>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/api/data")
def api_data():
    return jsonify(get_data())


if __name__ == "__main__":
    print("======================================")
    print("       MHE DASHBOARD SERVER")
    print("======================================")
    print("Starting dashboard...")
    print("Open: http://<RASPBERRY_PI_IP>:5000")
    print("======================================")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
