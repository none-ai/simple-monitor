"""
Simple Server Monitor
"""
from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/metrics')
def metrics():
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005)
