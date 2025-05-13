from flask import Flask, render_template
import requests

app = Flask(__name__)

SERVICES = {
    "Основной сайт": "https://astracat.vercel.app",
    "ASTRACAT DNS": "https://astracat-dns.vercel.app",
    "Генератор Xray VPN": "https://vpngen.vercel.app",
    "WARP генератор": "https://warp-liart.vercel.app",
    "ASTRACAT ShereVPN": "https://vpn-free-astra-net-v1.onrender.com"
}

def check_status(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except:
        return False

@app.route("/")
def index():
    statuses = {}
    for name, url in SERVICES.items():
        statuses[name] = "🟢 Онлайн" if check_status(url) else "🔴 Оффлайн"
    return render_template("index.html", statuses=statuses)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
