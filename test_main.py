from fastapi.testclient import TestClient
import pytest
from main import app
from unittest.mock import patch 
from unittest.mock import MagicMock

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


if __name__ == "__main__":
    pytest.main()