SAMPLE = {
    "title": "Lunch",
    "amount": 250.0,
    "type": "expense",
    "category": "Food",
    "date": "2026-11-10",
}


def create(client, headers):
    return client.post("/transactions", json=SAMPLE, headers=headers)


def test_create_transaction(client, auth_headers):
    res = create(client, auth_headers)
    assert res.status_code == 201
    assert res.json()["title"] == "Lunch"
    assert res.json()["amount"] == 250.0


def test_get_transactions(client, auth_headers):
    create(client, auth_headers)
    create(client, auth_headers)
    res = client.get("/transactions", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_specific_transaction(client, auth_headers):
    tid = create(client, auth_headers).json()["id"]
    res = client.get(f"/transactions/{tid}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["id"] == tid
    assert client.get("/transactions/9999", headers=auth_headers).status_code == 404


def test_update_transaction(client, auth_headers):
    tid = create(client, auth_headers).json()["id"]
    res = client.put(f"/transactions/{tid}", json={"amount": 300.0}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["amount"] == 300.0
    assert client.put("/transactions/9999", json={"amount": 1}, headers=auth_headers).status_code == 404


def test_delete_transaction(client, auth_headers):
    tid = create(client, auth_headers).json()["id"]
    res = client.delete(f"/transactions/{tid}", headers=auth_headers)
    assert res.status_code == 200
    assert client.get(f"/transactions/{tid}", headers=auth_headers).status_code == 404
    assert client.delete(f"/transactions/{tid}", headers=auth_headers).status_code == 404