def test_status_200_latest(client):
    res = client.get(
        "/latest",
        params={"from": "EUR"}
    )

    assert res["status_code"] == 200, (
        f"Code attendu 200, reçu {res['status_code']}"
    )

    return res["latency_ms"]


def test_content_type_json(client):
    res = client.get(
        "/latest",
        params={"from": "EUR"}
    )

    assert res["status_code"] == 200, (
        f"Code attendu 200, reçu {res['status_code']}"
    )

    content_type = res["response"].headers.get(
        "Content-Type", ""
    )

    assert "application/json" in content_type, (
        f"Content-Type invalide : {content_type}"
    )

    return res["latency_ms"]


def test_schema_keys(client):
    res = client.get(
        "/latest",
        params={"from": "EUR"}
    )

    assert res["status_code"] == 200, (
        f"Code attendu 200, reçu {res['status_code']}"
    )

    data = res["response"].json()

    for field in ["amount", "base", "date", "rates"]:
        assert field in data, (
            f"Champ manquant : {field}"
        )

    return res["latency_ms"]


def test_data_types(client):
    res = client.get(
        "/latest",
        params={"from": "EUR"}
    )

    assert res["status_code"] == 200, (
        f"Code attendu 200, reçu {res['status_code']}"
    )

    data = res["response"].json()

    assert isinstance(data["amount"], (int, float)), (
        "Le champ 'amount' doit être un nombre"
    )

    assert isinstance(data["base"], str), (
        "Le champ 'base' doit être une chaîne"
    )

    assert isinstance(data["date"], str), (
        "Le champ 'date' doit être une chaîne"
    )

    assert isinstance(data["rates"], dict), (
        "Le champ 'rates' doit être un objet"
    )

    return res["latency_ms"]


def test_usd_rate(client):
    res = client.get(
        "/latest",
        params={
            "from": "EUR",
            "to": "USD"
        }
    )

    assert res["status_code"] == 200, (
        f"Code attendu 200, reçu {res['status_code']}"
    )

    data = res["response"].json()

    assert "rates" in data, (
        "Champ 'rates' manquant"
    )

    assert "USD" in data["rates"], (
        "Le taux USD est absent"
    )

    assert isinstance(data["rates"]["USD"], (int, float)), (
        "Le taux USD doit être un nombre"
    )

    return res["latency_ms"]


def test_invalid_currency(client):
    res = client.get(
        "/latest",
        params={
            "from": "EUR",
            "to": "XXX"
        }
    )

    assert res["status_code"] >= 400, (
        f"Une erreur HTTP était attendue, reçu {res['status_code']}"
    )

    return res["latency_ms"]


ALL_TESTS = [
    (
        "GET /latest?from=EUR (Code 200)",
        test_status_200_latest
    ),
    (
        "Vérification Content-Type JSON",
        test_content_type_json
    ),
    (
        "Validation des champs obligatoires",
        test_schema_keys
    ),
    (
        "Validation des types de données",
        test_data_types
    ),
    (
        "Vérification du taux EUR → USD",
        test_usd_rate
    ),
    (
        "Gestion d'une devise invalide",
        test_invalid_currency
    ),
]
