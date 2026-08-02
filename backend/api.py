from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import subprocess
import sys
from datetime import datetime
import threading
import time

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app)

# File paths
BASE_DIR = os.path.dirname(__file__)
WAIKANE_TIDE_FILE = os.path.join(BASE_DIR, 'Waikane_Tide_Data.json')
WAIKANE_STREAM_FILE = os.path.join(BASE_DIR, 'Waikane_Stream_Data.json')
WAIAHOLE_STREAM_FILE = os.path.join(BASE_DIR, 'Waiahole_Stream_Data.json')
PUNALUU_STREAM_FILE = os.path.join(BASE_DIR, 'Punaluu_Stream_Data.json')
WAIKANE_TIDE_CURVE_FILE = os.path.join(BASE_DIR, 'Waikane_Tide_Curve.json')
RAIN_DATA_FILE = os.path.join(BASE_DIR, 'Rain_Data.json')
STREAM_TREND_DATA_FILE = os.path.join(BASE_DIR, 'Stream_Trend_Data.json')

# Caching / update control
CACHE_TTL_SECONDS = 300  # refresh at most every 5 minutes
_last_update_time = 0
_is_updating = False
_update_lock = threading.Lock()

def update_data():
    try:
        subprocess.run([sys.executable, "run_notebook.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print("Notebook execution failed:", e)
        return False


def _background_update():
    global _is_updating, _last_update_time
    with _update_lock:
        if _is_updating:
            return
        _is_updating = True
    try:
        success = update_data()
        if success:
            _last_update_time = time.time()
    finally:
        with _update_lock:
            _is_updating = False


def ensure_recent_data(force=False, blocking=False):
    """Ensure data is being updated at least once per CACHE_TTL_SECONDS.
    If force is True and blocking is True, run update synchronously.
    Otherwise start a background update when needed and return immediately.
    """
    global _last_update_time
    if force:
        if blocking:
            success = update_data()
            if success:
                _last_update_time = time.time()
            return
        # non-blocking force
        threading.Thread(target=_background_update, daemon=True).start()
        return

    # not forced: check TTL
    if time.time() - _last_update_time > CACHE_TTL_SECONDS:
        # start non-blocking update if not already running
        threading.Thread(target=_background_update, daemon=True).start()

@app.route('/api/waikane_tides', methods=['GET'])
def get_waikane_tide_data():
    ensure_recent_data()
    try:
        with open(WAIKANE_TIDE_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/waikane_stream', methods=['GET'])
def get_waikane_stream_data():
    ensure_recent_data()
    try:
        with open(WAIKANE_STREAM_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/waiahole_stream', methods=['GET'])
def get_waiahole_stream_data():
    ensure_recent_data()
    try:
        with open(WAIAHOLE_STREAM_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/punaluu_stream', methods=['GET'])
def get_punaluu_stream_data():
    ensure_recent_data()
    try:
        with open(PUNALUU_STREAM_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/waikane_tide_curve', methods=['GET'])
def get_waikane_tide_curve():
    ensure_recent_data()
    try:
        with open(WAIKANE_TIDE_CURVE_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/rain_data', methods=['GET'])
def get_rain_data():
    ensure_recent_data()
    try:    
        with open(RAIN_DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/stream_trend', methods=['GET'])
def get_stream_trend_data():
    ensure_recent_data()


@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Trigger an update. Use query param `blocking=true` for a synchronous update."""
    blocking = request.args.get('blocking', 'false').lower() in ('1', 'true', 'yes')
    ensure_recent_data(force=True, blocking=blocking)
    if blocking:
        return jsonify({"status": "updated", "timestamp": _last_update_time})
    return jsonify({"status": "update_started"})
    try:
        with open(STREAM_TREND_DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)