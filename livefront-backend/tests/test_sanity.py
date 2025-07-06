def test_client_and_health(client):
    assert client is not None
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}