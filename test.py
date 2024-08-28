import pytest
from fastapi.testclient import TestClient
import logging

from main import app


@pytest.fixture
def client():
    client = TestClient(app)
    client.delete("/notes/")
    return client


def test_create_note(client):
    note = {"title": "Test note", "content": "This is a test note"}
    response = client.post("/notes", json=note)
    assert response.status_code == 200


def test_get_notes(client):
    note = {"text": "Test note"}
    client.post("/notes", json=note)

    response = client.get("/notes")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_delete_all_notes(client):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    http_logger = logging.getLogger('http.client')
    http_logger.setLevel(logging.DEBUG)

    client.post("/notes", json={"title": "New note 1", "content": "Note text1"})
    client.post("/notes", json={"title": "New note 2", "content": "Note text 2"})

    logger.debug("Deleting all notes...")
    response = client.delete("/notes/")
    logger.debug(f"Delete response status code: {response.status_code}")
    assert response.status_code == 200

    logger.debug("Getting all notes after deletion...")
    response = client.get("/notes")
    logger.debug(f"Get response status code: {response.status_code}")
    logger.debug(f"Get response content: {response.json()}")
    assert response.status_code == 200
    assert len(response.json()['body']) == 2


def test_create_note_invalid(client):
    note = {"422_field": "Test note"}
    response = client.post("/notes", json=note)
    assert response.status_code == 422
