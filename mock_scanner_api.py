from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/vulnerabilities', methods=['GET'])
def get_vulnerabilities():
    mock_data = [
        {
            "source": "veracode",
            "severity": "high",
            "description": "SQL Injection in login form",
            "detected_on": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "remediation_status": "unresolved"
        },
        {
            "source": "qualys",
            "severity": "medium",
            "description": "Cross-site scripting in comments section",
            "detected_on": datetime.utcnow().isoformat(),
            "remediation_status": "unresolved"
        },
        {
            "source": "veracode",
            "severity": "low",
            "description": "Deprecated library usage",
            "detected_on": datetime.utcnow().isoformat(),
            "remediation_status": "resolved"
        }
    ]
    return jsonify(mock_data), 200

if __name__ == '__main__':
    app.run(port=5001)
