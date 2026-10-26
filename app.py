"""
Fleet Management - Vehicle Telemetry Ingestion Service (telemetry-core)
Release: v3.1.0-release
"""

import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Function to read telemetry configuration
def load_config(config_file="telemetry.conf"):
    config = {
        "TELEMETRY_PORT": 9092,
        "SERVICE_NAME": "telemetry-core",
        "RELEASE_VERSION": "v3.1.0-release",
        "ENVIRONMENT": "production"
    }
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k == "TELEMETRY_PORT":
                            config[k] = int(v)
                        else:
                            config[k] = v
        except Exception as e:
            print(f"[WARN] Error reading {config_file}: {e}")
    return config

CONFIG = load_config()
PORT = int(os.environ.get("PORT", CONFIG.get("TELEMETRY_PORT", 9092)))

# In-memory telemetry log for demo
telemetry_data_store = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fleet Management - Telemetry Core</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #0f172a; color: #f8fafc; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; padding: 40px; max-width: 650px; width: 100%; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5); text-align: center; }
        .badge { display: inline-block; background: #38bdf8; color: #0f172a; font-weight: bold; font-size: 13px; padding: 4px 12px; border-radius: 9999px; text-transform: uppercase; margin-bottom: 16px; letter-spacing: 0.5px; }
        h1 { font-size: 28px; margin-bottom: 12px; color: #ffffff; }
        p.subtitle { color: #94a3b8; font-size: 16px; margin-bottom: 24px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; text-align: left; }
        .item { background: #0f172a; padding: 14px 18px; border-radius: 10px; border: 1px solid #334155; }
        .item-label { font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: 600; }
        .item-value { font-size: 16px; color: #38bdf8; font-weight: bold; margin-top: 4px; }
        .status-dot { height: 10px; width: 10px; background-color: #22c55e; border-radius: 50%; display: inline-block; margin-right: 6px; }
        .footer { margin-top: 20px; color: #64748b; font-size: 13px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="badge">telemetry-core v3.1.0</div>
        <h1>Welcome to Fleet Management</h1>
        <p class="subtitle">Distributed Vehicle Telemetry Ingestion & Monitoring Service</p>
        <div class="grid">
            <div class="item">
                <div class="item-label">Status</div>
                <div class="item-value"><span class="status-dot"></span>Active / Listening</div>
            </div>
            <div class="item">
                <div class="item-label">Ingestion Port</div>
                <div class="item-value">{{ port }}</div>
            </div>
            <div class="item">
                <div class="item-label">Service Name</div>
                <div class="item-value">telemetry-core</div>
            </div>
            <div class="item">
                <div class="item-label">Release Tag</div>
                <div class="item-value">v3.1.0-release</div>
            </div>
        </div>
        <p style="color: #cbd5e1; font-size: 14px;">Automated CI/CD Pipeline & Ingestion Cluster Ready</p>
        <div class="footer">Commercial Fleet Tracking Organization &bull; DevOps Lab</div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE, port=PORT)

@app.route("/health", methods=["GET"])
@app.route("/status", methods=["GET"])
def health():
    return jsonify({
        "service": "telemetry-core",
        "status": "healthy",
        "version": "v3.1.0-release",
        "port": PORT,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

@app.route("/api/v1/telemetry", methods=["POST", "GET"])
def telemetry():
    if request.method == "POST":
        data = request.get_json(silent=True) or request.form.to_dict() or {}
        record = {
            "received_at": datetime.utcnow().isoformat() + "Z",
            "payload": data
        }
        telemetry_data_store.append(record)
        return jsonify({"message": "Telemetry data ingested successfully", "record": record}), 201
    return jsonify({"total_records": len(telemetry_data_store), "records": telemetry_data_store[-10:]})

def print_banner():
    banner = f"""
======================================================================
  WELCOME TO FLEET MANAGEMENT - VEHICLE TELEMETRY INGESTION SERVICE
======================================================================
 [SERVICE]     telemetry-core
 [VERSION]     v3.1.0-release
 [CONFIG]      telemetry.conf
 [PORT]        {PORT}
 [STATUS]      READY FOR DISTRIBUTED INGESTION
======================================================================
"""
    print(banner, flush=True)

if __name__ == "__main__":
    print_banner()
    print(f"[*] Starting Telemetry Core Service on http://0.0.0.0:{PORT} ...")
    app.run(host="0.0.0.0", port=PORT, debug=False)