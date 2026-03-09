"""
Simple Server Monitor
"""
import os
import time
from flask import Flask, jsonify
import psutil

app = Flask(__name__)

# Configuration
PORT = int(os.environ.get('PORT', 8005))
HOST = os.environ.get('HOST', '0.0.0.0')

def format_bytes(bytes_value):
    """Format bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def format_uptime(seconds):
    """Format uptime seconds to human readable format."""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if days > 0:
        return f"{days}d {hours}h {minutes}m {secs}s"
    elif hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    return f"{secs}s"

@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        # Quick check if we can get system info
        psutil.cpu_percent(interval=0.1)
        return jsonify({
            "status": "healthy",
            "service": "simple-monitor"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503

@app.route('/metrics')
def metrics():
    """Returns basic system metrics."""
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return jsonify({
            "cpu": {
                "percent": cpu,
                "count": psutil.cpu_count(),
                "physical_count": psutil.cpu_count(logical=False)
            },
            "memory": {
                "percent": memory.percent,
                "total": format_bytes(memory.total),
                "available": format_bytes(memory.available),
                "used": format_bytes(memory.used)
            },
            "disk": {
                "percent": disk.percent,
                "total": format_bytes(disk.total),
                "used": format_bytes(disk.used),
                "free": format_bytes(disk.free)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/network')
def network():
    """Returns network I/O statistics."""
    try:
        net_io = psutil.net_io_counters()
        per_nic = psutil.net_io_counters(pernic=True)

        return jsonify({
            "total": {
                "bytes_sent": format_bytes(net_io.bytes_sent),
                "bytes_recv": format_bytes(net_io.bytes_recv),
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout
            },
            "interfaces": {
                nic: {
                    "bytes_sent": format_bytes(data.bytes_sent),
                    "bytes_recv": format_bytes(data.bytes_recv),
                    "packets_sent": data.packets_sent,
                    "packets_recv": data.packets_recv
                }
                for nic, data in per_nic.items()
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/processes')
def processes():
    """Returns top processes by CPU and memory usage."""
    try:
        processes_list = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes_list.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort by CPU usage
        by_cpu = sorted(
            [p for p in processes_list if p.get('cpu_percent')],
            key=lambda x: x.get('cpu_percent', 0),
            reverse=True
        )[:10]

        # Sort by memory usage
        by_memory = sorted(
            [p for p in processes_list if p.get('memory_percent')],
            key=lambda x: x.get('memory_percent', 0),
            reverse=True
        )[:10]

        return jsonify({
            "by_cpu": by_cpu,
            "by_memory": by_memory,
            "total_processes": len(processes_list)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uptime')
def uptime():
    """Returns system uptime."""
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time

        return jsonify({
            "uptime_seconds": uptime_seconds,
            "uptime_formatted": format_uptime(uptime_seconds),
            "boot_time": boot_time,
            "boot_time_iso": psutil.datetime.fromtimestamp(boot_time)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/disk-io')
def disk_io():
    """Returns disk I/O statistics."""
    try:
        disk_io = psutil.disk_io_counters()

        return jsonify({
            "read_count": disk_io.read_count,
            "write_count": disk_io.write_count,
            "read_bytes": format_bytes(disk_io.read_bytes),
            "write_bytes": format_bytes(disk_io.write_bytes),
            "read_time": disk_io.read_time,
            "write_time": disk_io.write_time
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
