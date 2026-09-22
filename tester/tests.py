def test_status_200_valid_name(client):
    res = client.get("", params={"name": "michael"})
    assert res["status_code"] == 200, f"Code attendu 200, reçu {res['status_code']}"
    return res["latency_ms"]

def test_content_type_json(client):
    res = client.get("", params={"name": "michael"})
    assert res["ok"], f"Erreur réseau: {res['error']}"
    content_type = res["response"].headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Content-Type invalide: {content_type}"
    return res["latency_ms"]

def test_schema_keys(client):
    res = client.get("", params={"name": "michael"})
    data = res["response"].json()
    for field in ["name", "age", "count"]:
        assert field in data, f"Champ manquant: {field}"
    return res["latency_ms"]

def test_data_types(client):
    res = client.get("", params={"name": "michael"})
    data = res["response"].json()
    assert isinstance(data["name"], str), "Le champ 'name' doit être une string"
    assert data["age"] is None or isinstance(data["age"], int), "Le champ 'age' doit être un entier ou null"
    assert isinstance(data["count"], int), "Le champ 'count' doit être un entier"
    return res["latency_ms"]

def test_country_filter(client):
    res = client.get("", params={"name": "michael", "country_id": "FR"})
    assert res["status_code"] == 200, f"Code attendu 200, reçu {res['status_code']}"
    data = res["response"].json()
    assert data.get("country_id") == "FR", f"country_id attendu 'FR', reçu {data.get('country_id')}"
    return res["latency_ms"]

def test_missing_name_returns_422(client):
    res = client.get("", params={})
    assert res["status_code"] == 422, f"Code attendu 422 pour paramètre manquant, reçu {res['status_code']}"
    data = res["response"].json()
    assert "error" in data, "La réponse d'erreur doit contenir une clé 'error'"
    return res["latency_ms"]

ALL_TESTS = [
    ("GET /?name=michael (Code 200)", test_status_200_valid_name),
    ("Vérification Content-Type JSON", test_content_type_json),
    ("Validation des champs obligatoires", test_schema_keys),
    ("Validation des types de données", test_data_types),
    ("Filtrage par pays (country_id=FR)", test_country_filter),
    ("Gestion d'erreur sans paramètre (Code 422)", test_missing_name_returns_422),
]
