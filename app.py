import sys
import glob

import pandas as pd

from flask import Flask
from flask import jsonify

# list of dataframes
dfs = []

# Read the CSV files
for f in glob.glob("Firewall*.csv"):
    print("Reading file: [%s]" % f)
    local_df = pd.read_csv(f, low_memory=False)

    dfs.append(local_df)

full_df = pd.concat(dfs)
print("Data read complete.")

# Create a set of source IPs
source_ip_set = set(full_df["Source IP"])

# start the Flask app
app = Flask(__name__)

@app.route('/api/v1', methods=["GET"])
def info_view():
    """List of routes for this API."""
    output = {
        "info": "GET /api/v1",
        "list hosts": 'GET /api/v1/hosts',
        "list ports": 'GET /api/v1/ports',
        "connection details": 'GET /api/v1/hosts/<ip_addr>/connections',
    }
    return jsonify(output)

@app.route('/api/v1/hosts', methods=["GET"])
@app.route('/api/v1/hosts/', methods=["GET"])
def print_hosts():
    """Print the frequency of each IP address sourced in this data"""
    print("Printing hosts...")

    # Count up the number of times various IP addresses appear
    output_1 = {remote:count for remote, count in full_df["Source IP"].value_counts().items()}
    output_2 = {remote:count for remote, count in full_df["Destination IP"].value_counts().items()}

    # All the IP addresses we've seen
    all_ips = set(output_1.keys()).union(set(output_2.keys()))

    # Merge frequencies
    output = {a:output_1.get(a, 0) + output_2.get(a, 0) for a in all_ips}

    return jsonify(output)

@app.route('/api/v1/ports', methods=["GET"])
@app.route('/api/v1/ports/', methods=["GET"])
def print_ports():
    """Print the frequency of each IP address sourced in this data"""
    print("Printing ports...")

    # Count up the number of times various ports appear
    output_1 = {remote:count for remote, count in full_df["Source port"].value_counts().items()}
    output_2 = {remote:count for remote, count in full_df["Destination port"].value_counts().items()}

    # All the ports we've seen
    all_ports = set(output_1.keys()).union(set(output_2.keys()))

    # Merge frequencies
    output = {p:output_1.get(p, 0) + output_2.get(p, 0) for p in all_ports}

    return jsonify(output)

@app.route('/api/v1/hosts/<ip_addr>/connections', methods=["GET"])
@app.route('/api/v1/hosts/<ip_addr>/connections/', methods=["GET"])
def print_neighbors(ip_addr):
    """Get the adjacent nodes to which this IP address has connected"""
    print("Collecting data for source: [%s]" % ip_addr)

    output = {}
    if ip_addr in source_ip_set:

        rel_conns = full_df[full_df["Source IP"] == ip_addr]
        output_1 = {remote:count for remote, count in rel_conns["Destination IP"].value_counts().items()}

        rel_conns = full_df[full_df["Destination IP"] == ip_addr]
        output_2 = {remote:count for remote, count in rel_conns["Source IP"].value_counts().items()}

        # All the IP addresses we've seen
        all_ips = set(output_1.keys()).union(set(output_2.keys()))

        # Merge frequencies
        output = {a:output_1.get(a, 0) + output_2.get(a, 0) for a in all_ips}

    return jsonify(output)