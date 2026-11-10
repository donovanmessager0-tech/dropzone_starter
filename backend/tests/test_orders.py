# backend/tests/test_orders.py
from datetime import datetime, timezone, timedelta

def test_order_decrements_stock_and_marks_sold_out(client, make_drop):
    # Crée un drop avec 1 seul article en stock
    drop = make_drop(stock=1, start_time=datetime.now(timezone.utc) - timedelta(hours=1))
    
    response = client.post(f"/api/drops/{drop['id']}/orders")
    assert response.status_code == 200
    data = response.json()
    assert data["remaining"] == 0
    assert data["status"] == "sold_out"

def test_order_refused_when_sold_out(client, make_drop):
    drop = make_drop(stock=0, start_time=datetime.now(timezone.utc) - timedelta(hours=1))
    
    response = client.post(f"/api/drops/{drop['id']}/orders")
    assert response.status_code == 400

def test_order_refused_when_not_yet_open(client, make_drop):
    drop = make_drop(stock=5, start_time=datetime.now(timezone.utc) - timedelta(hours=1)) # Erreur, on veut futur
    # Mettons un start_time dans le futur
    # (Ajustez selon votre fixture make_drop si besoin de passer le start_time explicitement)
    future_drop = make_drop(stock=5, start_time=datetime.now(timezone.utc) + timedelta(hours=1))
    
    response = client.post(f"/api/drops/{future_drop['id']}/orders")
    assert response.status_code == 400

def test_order_unknown_drop(client):
    response = client.post("/api/drops/999999/orders")
    assert response.status_code == 404
