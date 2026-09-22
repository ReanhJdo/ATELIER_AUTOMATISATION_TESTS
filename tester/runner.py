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

            results.append({
                "name": name,
                "status": "PASS",
                "latency_ms": latency,
                "details": ""
            })

        except AssertionError as exc:
            failed += 1

            results.append({
                "name": name,
                "status": "FAIL",
                "latency_ms": 0.0,
                "details": str(exc)
            })

        except Exception as exc:
            failed += 1

            results.append({
                "name": name,
                "status": "FAIL",
                "latency_ms": 0.0,
                "details": f"Erreur inattendue : {str(exc)}"
            })

    total = passed + failed

    error_rate = (
        round(failed / total, 3)
        if total > 0
        else 0.0
    )

    if latencies:
        avg_latency = round(
            sum(latencies) / len(latencies),
            2
        )

        sorted_latencies = sorted(latencies)

        index = int(0.95 * len(sorted_latencies))

        index = min(
            index,
            len(sorted_latencies) - 1
        )

        p95_latency = sorted_latencies[index]

    else:
        avg_latency = 0.0
        p95_latency = 0.0

    return {
        "api": "Frankfurter",

        "timestamp": datetime.now(
            timezone.utc
        ).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),

        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": error_rate,
            "latency_ms_avg": avg_latency,
            "latency_ms_p95": p95_latency
        },

        "tests": results
    }
