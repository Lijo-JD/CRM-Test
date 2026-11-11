from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_dashboard_route(monkeypatch):
    monkeypatch.setattr('app.api.routes.dashboard.get_dashboard_summary', lambda: {'customer_count': 3})
    response = client.get('/api/v1/dashboard')
    assert response.status_code == 200
    assert response.json()['customer_count'] == 3
