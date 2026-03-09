# Simple Monitor

A lightweight Flask-based server monitoring application that provides real-time system metrics via REST API.

## Features

- Health check endpoint
- System metrics (CPU, Memory, Disk)
- Network statistics
- Process monitoring
- System uptime
- Disk I/O statistics

## API Endpoints

### Health Check
```
GET /health
```
Returns the service health status.

### Metrics
```
GET /metrics
```
Returns comprehensive system metrics including:
- CPU usage percentage
- Memory usage percentage
- Disk usage percentage

### Network
```
GET /network
```
Returns network I/O statistics.

### Processes
```
GET /processes
```
Returns top processes by CPU and memory usage.

### Uptime
```
GET /uptime
```
Returns system uptime information.

### Disk I/O
```
GET /disk-io
```
Returns disk I/O statistics.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

The server will start on `http://0.0.0.0:8005`

## Configuration

Configure via environment variables:
- `PORT`: Server port (default: 8005)
- `HOST`: Server host (default: 0.0.0.0)

## Tech Stack

- Flask
- psutil

作者: stlin256的openclaw
