import os
import time
import requests


class HttpClient:

    def __init__(self, base_url="https://api.agify.io", timeout=5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.api_key = os.getenv("AGIFY_API_KEY")

    def get(self, endpoint="", params=None):
        url = f"{self.base_url}{endpoint}"

        params = params.copy() if params else {}

        if self.api_key:
            params["apikey"] = self.api_key

        max_attempts = 2
        last_exception = None
        latency_ms = 0.0

        for attempt in range(max_attempts):
            start = time.perf_counter()

            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )

                latency_ms = round(
                    (time.perf_counter() - start) * 1000,
                    2
                )

                if response.status_code == 429:
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                        continue

                    return {
                        "ok": False,
                        "status_code": 429,
                        "latency_ms": latency_ms,
                        "response": response,
                        "error": "Rate limit Agify (429)"
                    }

                if response.status_code >= 500:
                    if attempt < max_attempts - 1:
                        time.sleep(1)
                        continue

                return {
                    "ok": True,
                    "status_code": response.status_code,
                    "latency_ms": latency_ms,
                    "response": response,
                    "error": None
                }

            except requests.RequestException as exc:
                latency_ms = round(
                    (time.perf_counter() - start) * 1000,
                    2
                )

                last_exception = exc

                if attempt < max_attempts - 1:
                    time.sleep(1)

        return {
            "ok": False,
            "status_code": 0,
            "latency_ms": latency_ms,
            "response": None,
            "error": str(last_exception)
        }
