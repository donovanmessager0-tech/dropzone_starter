from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from tests.conftest import iso


def test_order_decrements_stock_and_marks_sold_out(
    client: TestClient, make_drop
) -> None:
    drop = make_drop(stock=1)

    response = client.post(f"/drops/{drop['id']}/orders")

    assert response.status_code == 201
    data = response.json()
    assert data["drop"]["remaining"] == 0
    assert data["drop"]["status"] == "sold_out"
    assert isinstance(data["created_at"], str)


def test_order_refused_when_sold_out(client: TestClient, make_drop) -> None:
    drop = make_drop(stock=1)
    first = client.post(f"/drops/{drop['id']}/orders")
    assert first.status_code == 201

    second = client.post(f"/drops/{drop['id']}/orders")
    assert second.status_code == 409


def test_order_refused_when_not_yet_open(client: TestClient, make_drop) -> None:
    future_opens_at = iso(datetime.now(UTC) + timedelta(hours=1))
    drop = make_drop(stock=5, opens_at=future_opens_at)

    response = client.post(f"/drops/{drop['id']}/orders")

    assert response.status_code == 409


def test_order_unknown_drop(client: TestClient) -> None:
    response = client.post("/drops/999999/orders")

    assert response.status_code == 404
