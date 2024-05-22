from dotenv import load_dotenv
import os
from flask import Flask, render_template, jsonify
from pymongo import MongoClient

load_dotenv(".env.local")
load_dotenv(".env")

app = Flask(__name__)

db = MongoClient(os.getenv('MONGODB_CONNECT_URL')).get_database()
collection = db['alerts']

def process_alerts(alerts):
    processed_alerts = []
    for alert in alerts:
        severity = alert.get('alert', {}).get('severity', 3)
        severity_class = 'bg-white'  # Default to normal
        if severity == 1:
            severity_class = 'bg-red-500'
        elif severity == 2:
            severity_class = 'bg-yellow-500'
        
        processed_alerts.append({
            'timestamp': alert.get('timestamp'),
            'src_ip': alert.get('src_ip'),
            'dest_ip': alert.get('dest_ip'),
            'signature': alert.get('alert', {}).get('signature'),
            'category': alert.get('alert', {}).get('category'),
            'severity': alert.get('alert', {}).get('severity'),
            'severity_class': severity_class
        })
    return processed_alerts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alerts')
def alerts():
    alerts = list(collection.find().sort('timestamp', -1).limit(100))
    alerts = process_alerts(alerts)
    return jsonify(alerts)

if __name__ == '__main__':
    app.run(debug=True)