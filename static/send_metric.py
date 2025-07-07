#!/usr/bin/env python3

import requests
import time
import json
import random
import uuid
import argparse

# Lista de hosts aleatórios
HOSTS = [
    'api.d.com', 'sandbox-cert.d.com', 'api-certs.d.com',
    'amazon.d.com', 'microsoft.d.com', 'microsoft-sandbox.d.com',
    'apple.d.com', 'apple-sandbox.d.com'
]

STATUSES = ['200', '403', '500']
METHODS = ['GET', 'POST', 'PUT']
GEOIP = 'Uruguay'

def generate_payload(merchantid=None):
    host = random.choice(HOSTS)
    method = random.choice(METHODS)
    status = random.choice(STATUSES)
    uri = f"/v1/transactions/{random.randint(1000,9999)}"
    reason = "blocked" if status == "403" else "ok"
    mid = merchantid or str(uuid.uuid4())

    payload = {
        "resourceMetrics": [
            {
                "resource": {
                    "attributes": [
                        {"key": "host", "value": {"stringValue": host}},
                        {"key": "merchantid", "value": {"stringValue": mid}},
                        {"key": "geoip_city_country_name", "value": {"stringValue": GEOIP}},
                        {"key": "method", "value": {"stringValue": method}},
                        {"key": "uri", "value": {"stringValue": uri}},
                        {"key": "status", "value": {"stringValue": status}},
                        {"key": "reason", "value": {"stringValue": reason}},
                    ]
                },
                "scopeMetrics": [
                    {
                        "metrics": [
                            {
                                "name": "waf.request.count",
                                "type": "gauge",
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "asDouble": 1.0,
                                            "timeUnixNano": str(int(time.time() * 1e9))
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return payload

def main():
    parser = argparse.ArgumentParser(description="Send synthetic OTLP metrics to a Collector.")
    parser.add_argument("--endpoint", default="http://localhost:4318/v1/metrics", help="OTLP HTTP endpoint")
    parser.add_argument("--count", type=int, default=5, help="How many metrics to send")
    parser.add_argument("--interval", type=float, default=1.0, help="Interval between sends (seconds)")
    parser.add_argument("--merchantid", help="Use fixed merchantid (optional)")
    args = parser.parse_args()

    for i in range(args.count):
        payload = generate_payload(args.merchantid)
        response = requests.post(
            args.endpoint,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        print(f"[{i+1}/{args.count}] Sent -> Status: {response.status_code}")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
