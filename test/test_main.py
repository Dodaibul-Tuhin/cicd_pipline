from fastapi.testclient import TestClient
from main import api, tickets, Ticket

client = TestClient(api)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}


def test_add_ticket():
    tickets.clear()  # Reset before test
    new_ticket = {
        "id": 1,
        "flight_name": "Air Asia",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Singapore"
    }
    response = client.post("/ticket", json=new_ticket)
    assert response.status_code == 200
    assert response.json() == new_ticket


def test_get_tickets():
    response = client.get("/ticket")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_update_ticket():
    updated_ticket = {
        "id": 1,
        "flight_name": "Air Asia Updated",
        "flight_date": "2025-10-16",
        "flight_time": "15:30",
        "destination": "Bangkok"
    }
    response = client.put("/ticket/1", json=updated_ticket)
    assert response.status_code == 200
    assert response.json() == updated_ticket


def test_delete_ticket():
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    deleted_ticket = response.json()
    assert deleted_ticket["id"] == 1
    # After deletion, list should be empty
    assert len(tickets) == 0


def test_delete_nonexistent_ticket():
    response = client.delete("/ticket/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket not found, deletion failed"}
