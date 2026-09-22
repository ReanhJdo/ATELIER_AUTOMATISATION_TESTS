from datetime import datetime, timezone
from tester.client import HttpClient
from tester.tests import ALL_TESTS

def run_all_tests():
    client = HttpClient()
    results = []
    latencies = []
    passed = 0
    failed = 0

    for name, test_func in ALL_TESTS:
        try:
            latency = test_func(client)
            latencies.append(latency)
            passed += 1
            results.append({"name": name, "status": "PASS", "latency_ms": latency, "details": ""})
        except AssertionError as exc:
            failed += 1
            results.append({"name": name, "status": "FAIL", "latency_ms": 0.0, "details": str(exc)})
        except Exception as exc:
            failed += 1
            results.append({"name": name, "status": "FAIL", "latency_ms": 0.0, "details": f"Erreur: {str(exc)}"})

    total = passed + failed
    error_rate = round(failed / total, 3) if total > 0 else 0.0
    avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else 0.0

    # Calcul P95 natif (sans bibliothèque externe)
    if latencies:
        sorted_lat = sorted(latencies)
        idx = int(0.95 * len(sorted_lat))
        p95_latency = sorted_lat[min(idx, len(sorted_lat) - 1)]
    else:
        p95_latency = 0.0

    return {
        "api": "Agify",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": error_rate,
            "latency_ms_avg": avg_latency,
            "latency_ms_p95": p95_latency,
        },
        "tests": results
    }
