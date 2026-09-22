import time
import requests


class HttpClient:

    def __init__(self, base_url="https://api.frankfurter.app", timeout=5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, endpoint="", params=None):
        url = f"{self.base_url}{endpoint}"

        attempts = 0
        last_exception = None
        latency_ms = 0.0

        while attempts < 2:
            attempts += 1
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

                # Retry simple en cas de limitation
                if response.status_code == 429 and attempts < 2:
                    time.sleep(1)
                    continue

                # Retry simple en cas d'erreur serveur
                if response.status_code >= 500 and attempts < 2:
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

                if attempts < 2:
                    time.sleep(1)

        return {
            "ok": False,
            "status_code": 0,
            "latency_ms": latency_ms,
            "response": None,
            "error": str(last_exception)
        }
