from flask import Flask, render_template
import cloudscraper
import socket

app = Flask(__name__)
scraper = cloudscraper.create_scraper()

SERVICES = {
    "Основной сайт ASTRACAT": "https://astracat.vercel.app",
    "ASTRACAT DNS": "https://astracat-dns.vercel.app",
    "Генератор Xray VPN": "https://vpngen.vercel.app",
    "WARP генератор": "https://warp-liart.vercel.app",
    "ASTRACAT ShereVPN": "https://vpn-free-astra-net-v1.onrender.com"
}

def dns_check(hostname):
    try:
        socket.gethostbyname(hostname)
        return True
    except:
        return False

def check_status(url):
    try:
        response = scraper.get(url, timeout=5)
        return response.status_code == 200
    except:
        # fallback: DNS check
        hostname = url.split("//")[-1].split("/")[0]
        return dns_check(hostname)

@app.route("/")
def index():
    statuses = {}
    for name, url in SERVICES.items():
        statuses[name] = "🟢 В сети" if check_status(url) else "🔴 Не работает"
    return render_template("index.html", statuses=statuses)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
