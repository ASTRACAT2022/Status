from flask import Flask, render_template
import socket
import subprocess
import platform
import re

app = Flask(__name__)

SERVICES = {
    "Основной сайт ASTRACAT": "astracat.vercel.app",
    "ASTRACAT DNS": "astracat-dns.vercel.app",
    "Генератор Xray VPN": "vpngen.vercel.app",
    "WARP генератор": "warp-liart.vercel.app",
    "ASTRACAT ShereVPN": "vpn-free-astra-net-v1.onrender.com",
    "Сервер 85.209.2.112": "85.209.2.112"
}

def is_ip(hostname):
    return all(part.isdigit() and 0 <= int(part) <= 255 for part in hostname.split('.') if part)

def ping_host(hostname):
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        result = subprocess.run(['ping', param, '1', hostname], capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            output = result.stdout
            match = re.search(r'time[=<]?\s?(\d+\.?\d*)\s?ms', output)
            if match:
                return f"🟢 {match.group(1)} ms"
            else:
                return "🟢 В сети"
        else:
            return "🔴 Не работает"
    except:
        return "🔴 Не работает"

def check_status(hostname):
    try:
        if is_ip(hostname):
            return ping_host(hostname)
        else:
            socket.gethostbyname(hostname)
            return "🟢 В сети"
    except:
        return "🔴 Не работает"

@app.route("/")
def index():
    statuses = {}
    for name, host in SERVICES.items():
        statuses[name] = check_status(host)
    return render_template("index.html", statuses=statuses)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
