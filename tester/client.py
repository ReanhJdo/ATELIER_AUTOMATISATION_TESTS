import time
import requests


class HttpClient:

    def __init__(self, base_url="https://api.agify.io", timeout=5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, endpoint="", params=None):

        url = f"{self.base_url}{endpoint}"

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

                # Gestion du 429
                if response.status_code == 429:

                    # Agify indique le temps avant le reset
                    reset = response.headers.get(
                        "X-Rate-Limit-Reset"
                    )

                    if attempt < max_attempts - 1:

                        if reset:
                            try:
                                wait_time = float(reset)

                                # On évite une attente énorme
                                # pendant le TP
                                wait_time = min(wait_time, 5.0)

                            except ValueError:
                                wait_time = 2.0
                        else:
                            wait_time = 2.0

                        time.sleep(wait_time)
                        continue

                    return {
                        "ok": False,
                        "status_code": 429,
                        "latency_ms": latency_ms,
                        "response": response,
                        "error": "Rate limit Agify (429)"
                    }

                # Retry sur erreurs serveur
                if response.status_code >= 500:

                    if attempt < max_attempts - 1:
                        time.sleep(1.0)
                        continue

                return {
                    "ok": True,
                    "status_code": response.status_code,
                    "latency_ms": latency_ms,
                    "response": response,
                    "error": None
                }

            except requests.Timeout as exc:

                latency_ms = round(
                    (time.perf_counter() - start) * 1000,
                    2
                )

                last_exception = exc

                if attempt < max_attempts - 1:
                    time.sleep(1.0)

            except requests.RequestException as exc:

                latency_ms = round(
                    (time.perf_counter() - start) * 1000,
                    2
                )

                last_exception = exc

                if attempt < max_attempts - 1:
                    time.sleep(1.0)

        return {
            "ok": False,
            "status_code": 0,
            "latency_ms": latency_ms,
            "response": None,
            "error": str(last_exception)
        }
