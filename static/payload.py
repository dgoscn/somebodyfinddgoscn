import json, time, requests

payload = {
  "resourceMetrics": [
    {
      "resource": {
        "attributes": [
          {"key": "merchantid", "value": {"stringValue": "merchant-abc"}}
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

res = requests.post(
    "http://localhost:4318/v1/metrics",
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload)
)

print("Status:", res.status_code)
print("Resposta:", res.text)
