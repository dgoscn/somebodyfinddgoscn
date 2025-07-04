import json
import time
import requests

def convert_to_otlp(log):
    merchantid = log.get("headers", {}).get("x-login", "unknown")
    now = int(time.time() * 1e9)

    otlp = {
        "resourceMetrics": [
            {
                "resource": {
                    "attributes": [
                        {"key": "merchantid", "value": {"stringValue": merchantid}}
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
                                            "timeUnixNano": str(now)
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

    return otlp

def main():
    with open("logs/log1.json") as f:
        log = json.load(f)

    payload = convert_to_otlp(log)

    response = requests.post(
        "http://localhost:4318/v1/metrics",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    main()
