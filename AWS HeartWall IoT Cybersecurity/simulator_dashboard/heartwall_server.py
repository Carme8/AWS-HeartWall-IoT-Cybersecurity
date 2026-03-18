"""
╔══════════════════════════════════════════════════════════════╗
║   AWS HeartWall — Super Server v3.0                          ║
║   Bridge Dashboard + AWS S3 Synchronization                  ║
║                                                              ║
║   Avvio:  python heartwall_server.py                         ║
║                                                              ║
║   !! APRI NEL BROWSER: http://localhost:5000 !!              ║
║   (NON aprire l'HTML come file — usa questo URL)             ║
║                                                              ║
║   GET  /           → serve heartwall_bridge.html             ║
║   GET  /stats      → dati dashboard (poll 2s)                ║
║   POST /attack     → {"mode": "none|cmd|bio|combo"}          ║
║   GET  /health     → health check                            ║
╚══════════════════════════════════════════════════════════════╝
"""

import boto3
import json
import time
import random
import threading
import math
import os
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ── CONFIGURAZIONE AWS / LOCALSTACK ──────────────────────────
# Per AWS reale: rimuovi endpoint_url e configura ~/.aws/credentials
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',   # LocalStack
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

BUCKET_NAME = "heartwall-telemetry"

try:
    s3_client.create_bucket(Bucket=BUCKET_NAME)
    print(f"[AWS] Bucket '{BUCKET_NAME}' creato/verificato.")
except Exception as e:
    print(f"[AWS] Bucket già esistente o LocalStack non attivo: {e}")


# ── STATO GLOBALE ─────────────────────────────────────────────
state = {
    "attack_mode":   "none",  # none | cmd | bio | combo
    "tick":          0,
    "last_aws_sync": 0,
}
lock = threading.Lock()

def background_tick():
    while True:
        with lock:
            state["tick"] += 1
        time.sleep(0.1)

threading.Thread(target=background_tick, daemon=True).start()


# ── SYNC S3 ───────────────────────────────────────────────────
def sync_to_aws(data, is_malicious):
    try:
        tag       = "ATTACK" if is_malicious else "NORMAL"
        file_name = f"telemetry_{tag}_{datetime.now().strftime('%H%M%S')}.json"
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(data),
            ContentType='application/json'
        )
        print(f"  [AWS] Sincronizzazione completata: {file_name}")
    except Exception as e:
        print(f"  [AWS] Errore sincronizzazione: {e}")


# ═════════════════════════════════════════════════════════════
# GET /  →  serve la dashboard HTML
# !! SOLUZIONE al problema file:// vs localhost !!
# Apri http://localhost:5000 invece di aprire l'HTML direttamente
# ═════════════════════════════════════════════════════════════
@app.route("/")
def dashboard():
    html_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(html_dir, "heartwall_bridge.html")


# ═════════════════════════════════════════════════════════════
# GET /stats  →  dati per la dashboard (poll ogni 2s)
# ═════════════════════════════════════════════════════════════
@app.route("/stats")
def get_stats():
    with lock:
        mode = state["attack_mode"]
        tick = state["tick"]

    # ── Valori base NORMALE ───────────────────────────────────
    hr           = 72 + round(random.gauss(0, 2))
    rr           = round(60000 / max(hr, 1))
    qrs          = 88 + round(random.gauss(0, 3))
    qt           = 390 + round(random.gauss(0, 5))
    volt         = round(random.uniform(3.1, 3.3), 2)
    anomaly      = round(random.uniform(0.04, 0.18), 3)
    cmd_score    = round(random.uniform(0.01, 0.08), 3)
    bio_score    = round(random.uniform(0.01, 0.06), 3)
    mqtt_pkt     = round(random.uniform(1.1, 1.4), 1)
    infer_ms     = round(random.uniform(2.8, 4.2), 1)
    is_malicious = 0
    status       = "NORMAL"

    # ── Modalità BIO TAMPERING ────────────────────────────────
    if mode == "bio":
        hr           = 72           # fisso — segnale replay impossibile
        rr           = 833          # 60000/72 esatto — biologicamente impossibile
        qrs          = 88
        qt           = 390
        volt         = round(random.uniform(1.5, 2.0), 2)
        anomaly      = round(random.uniform(0.86, 0.96), 3)
        cmd_score    = round(random.uniform(0.01, 0.05), 3)
        bio_score    = round(random.uniform(0.88, 0.97), 3)
        mqtt_pkt     = round(random.uniform(1.0, 1.2), 1)
        infer_ms     = round(random.uniform(1.0, 1.5), 1)
        is_malicious = 1
        status       = "BIO_TAMPER"

    # ── Modalità CMD INJECTION ────────────────────────────────
    elif mode == "cmd":
        hr           = random.randint(100, 135)
        rr           = round(60000 / max(hr, 1))
        qrs          = random.randint(110, 140)
        qt           = random.randint(440, 490)
        volt         = round(random.uniform(3.0, 3.4), 2)
        anomaly      = round(random.uniform(0.80, 0.97), 3)
        cmd_score    = round(random.uniform(0.85, 0.97), 3)
        bio_score    = round(random.uniform(0.01, 0.06), 3)
        mqtt_pkt     = round(random.uniform(4.5, 7.2), 1)
        infer_ms     = round(random.uniform(1.1, 1.8), 1)
        is_malicious = 1
        status       = "CMD_INJECTION"

    # ── Modalità COMBO ────────────────────────────────────────
    elif mode == "combo":
        hr           = random.randint(220, 280)
        rr           = round(60000 / max(hr, 1))
        qrs          = random.randint(125, 160)
        qt           = random.randint(460, 510)
        volt         = 4.5                          # Overvolt pericoloso
        anomaly      = round(random.uniform(0.91, 0.99), 3)
        cmd_score    = round(random.uniform(0.80, 0.95), 3)
        bio_score    = round(random.uniform(0.75, 0.90), 3)
        mqtt_pkt     = round(random.uniform(6.0, 9.5), 1)
        infer_ms     = round(random.uniform(0.8, 1.2), 1)
        is_malicious = 1
        status       = "CRITICAL_COMBO"

    normal_score = round(max(0.0, 1.0 - anomaly), 3)

    # ── Payload completo (tutti i campi attesi dalla dashboard) ─
    payload = {
        # Identità dispositivo
        "device_id":    "HW-PM-001",
        "timestamp":    datetime.now().isoformat(),
        "tick":         tick,

        # Vitali ECG — attesi dalla dashboard
        "heart_rate":   hr,
        "rr_interval":  rr,
        "qrs_ms":       qrs,
        "qt_interval":  qt,

        # Hardware AWS
        "voltage":      volt,
        "ecg_wave":     [math.sin((tick + i) * 0.5) * 10 for i in range(20)],

        # Score ML — attesi dalla dashboard
        "anomaly_score":  anomaly,
        "cmd_score":      cmd_score,
        "bio_score":      bio_score,
        "normal_score":   normal_score,

        # Classificazione — attesi dalla dashboard
        "is_malicious":   is_malicious,
        "attack_mode":    mode,    # none | cmd | bio | combo
        "threat_type":    status,  # NORMAL | CMD_INJECTION | BIO_TAMPER | CRITICAL_COMBO
        "status":         status,  # alias mantenuto

        # Infrastruttura
        "mqtt_pkt_min": mqtt_pkt,
        "inference_ms": infer_ms,
        "uptime_sla":   "99.97%",
    }

    # ── Sync S3 ogni ~2s in background ────────────────────────
    now = time.time()
    if now - state["last_aws_sync"] > 2:
        threading.Thread(
            target=sync_to_aws,
            args=(payload, bool(is_malicious)),
            daemon=True
        ).start()
        state["last_aws_sync"] = now

    return jsonify(payload)


# ═════════════════════════════════════════════════════════════
# POST /attack  →  pulsanti della dashboard
# body: {"mode": "cmd"} | {"mode": "bio"} | {"mode": "combo"} | {"mode": "none"}
# ═════════════════════════════════════════════════════════════
@app.route("/attack", methods=["POST"])
def set_attack():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "none")
    if mode not in ("none", "cmd", "bio", "combo"):
        return jsonify({"error": f"mode '{mode}' non valido"}), 400
    with lock:
        state["attack_mode"] = mode
    labels = {
        "none":  "NORMALE ✓",
        "cmd":   "CMD INJECTION ⚡",
        "bio":   "BIO TAMPER ⬤",
        "combo": "COMBO P0 ☢"
    }
    print(f"\n!!! CAMBIO MODALITÀ → {labels.get(mode)} !!!\n")
    return jsonify({"ok": True, "mode": mode})


# ═════════════════════════════════════════════════════════════
# GET /health
# ═════════════════════════════════════════════════════════════
@app.route("/health")
def health():
    return jsonify({
        "status":      "ok",
        "server":      "HeartWall Super Server v3.0",
        "attack_mode": state["attack_mode"],
        "tick":        state["tick"],
        "aws_bucket":  BUCKET_NAME,
    })


# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════╗")
    print("║    AWS HEARTWALL — SUPER SERVER v3.0 AVVIATO    ║")
    print("║   Bridge Dashboard + AWS S3 Synchronization     ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║  !! APRI NEL BROWSER: http://localhost:5000 !!  ║")
    print("║  (non aprire l'HTML come file doppio-click)     ║")
    print("╚══════════════════════════════════════════════════╝")
    app.run(host="0.0.0.0", port=5000, debug=False)