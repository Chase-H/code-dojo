import pytest
from fastapi.testclient import TestClient
from example_two import app, get_db, create_db, Base, Engine, Animal
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine


@pytest.fixture
def client():
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}


def test_insert_animal(client):
    animal = {
        "name": "Doggo",
        "species": "Dog",
        "age": 5
    }
    response = client.post("/api/v1/animals", json=animal)
    assert response.status_code == 200
    assert response.json()["animal"]["name"] == "Doggo"


def test_read_animals(client):
    animal = {
        "name": "Doggo",
        "species": "Dog",
        "age": 5
    }
    response = client.post("/api/v1/animals", json=animal)
    response = client.get("/api/v1/animals")
    assert response.status_code == 200
    assert len(response.json()["animals"]) > 0


def test_read_animal(client):
    animal_id = 1
    response = client.get(f"/api/v1/animals/{animal_id}")
    assert response.status_code == 400
    assert response.json()["detail"] == f"Could not find animal with id: {animal_id}"


def test_update_animal(client):
    animal_id = 1
    updated_animal = {
        "name": "Updated Doggo",
        "species": "Dog",
        "age": 6
    }
    response = client.put(f"/api/v1/animals/{animal_id}", json=updated_animal)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == f"Could not find animal with id: {animal_id}"


def test_update_animal_name(client):
    animal_id = 1
    updated_animal = {
        "name": "New Name",
    }
    response = client.patch(f"/api/v1/animals/{animal_id}", json=updated_animal)
    assert response.status_code == 400
    assert response.json()["detail"] == f"Could not find animal with id: {animal_id}"


def test_delete_item(client):
    animal_id = 1
    response = client.delete(f"/api/v1/animals/{animal_id}")
    assert response.status_code == 400
    assert response.json()["detail"] == f"Could not find animal with id: {animal_id}"
