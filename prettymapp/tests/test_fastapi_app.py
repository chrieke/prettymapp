from fastapi.testclient import TestClient
from prettymapp.fastapi_app import app

client = TestClient(app)

def test_map_image_valid_params():
    response = client.get("/map_image?lat=52.52&lon=13.405&radius=1000&style=Peach")
    assert response.status_code == 200
    assert "image_url" in response.json()

def test_map_image_invalid_style():
    response = client.get("/map_image?lat=52.52&lon=13.405&radius=1000&style=InvalidStyle")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid style parameter"}

def test_map_image_missing_params():
    response = client.get("/map_image?lat=52.52&lon=13.405")
    assert response.status_code == 422
