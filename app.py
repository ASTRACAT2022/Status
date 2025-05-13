from flask import Flask, render_template
import socket
import subprocess
import platform
import re
import time
import json

app = Flask(__name__)

LOG_FILE = "ping_log.json"
PING_TARGET = "85.209.2.112"

def ping_latency(hostname):
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        result = subprocess.run(['ping', param, '1', hostname], capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            output = result.stdout
            match = re.search(r'time[=<]?\s?(\d+\.?\d*)\s?ms', output)
            if match:
                return float(match.group(1))
    except:
        return None
    return None

def log_latency(latency):
    timestamp = int(time.time())
    log = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                log = json.load(f)
        except:
            pass
    log.append({"time": timestamp, "latency": latency if latency is not None else 0})
    log = log[-50:]  # максимум 50 точек
    with open(LOG_FILE, "w") as f:
        json.dump(log, f)

@app.route("/")
def index():
    latency = ping_latency(PING_TARGET)
    log_latency(latency)
    return render_template("index.html", latency=latency)

@app.route("/chart")
def chart():
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []
    return render_template("chart.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
