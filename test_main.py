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


    # Mocking Firebase Auth - SignUp functionality
@patch('main.auth.create_user')
def test_signup(mock_create_user):
    # Simulate successful user creation
    mock_user = MagicMock()
    mock_user.uid = "12345"
    mock_user.email = "testuser@example.com"
    mock_create_user.return_value = mock_user

    # Sample user data to test SignUp
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }

    # Call the SignUp endpoint
    response = client.post("/SignUp", json=user_data)

    # Check if the response status code is 201 (Created)
    assert response.status_code == 201

    # Check if the response contains the expected message and user_id
    response_json = response.json()
    assert response_json["message"] == "User created successfully"
    assert response_json["user_id"] == "12345"


#Test caeses for signIn
@patch("main.firebase.auth")
def test_sign_in_success(mock_auth):
    mock_auth().sign_in_with_email_and_password.return_value = {
        "idToken": "fake_token_123"
    }

    response = client.post("/SignIn", json={
        "email": "testuser@example.com",
        "password": "testpassword123"
    })

    assert response.status_code == 200
    assert response.json() == {
        "message": "User signed in successfully",
        "token": "fake_token_123"
    }



# Test case: invalid credentials
@patch("main.firebase.auth")
def test_sign_in_invalid_credentials(mock_auth):
    mock_auth().sign_in_with_email_and_password.side_effect = Exception("Invalid credentials")

    response = client.post("/SignIn", json={
        "email": "wrong@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid credentials"
    }


#Test Cases for valid token
@patch("main.auth.verify_id_token")
def test_validate_token_success(mock_verify):
    mock_verify.return_value = {"uid": "12345"}

    headers = {
        "Authorization": "valid_token_123"
    }

    response = client.post("/validate_token", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "message": "Token is valid",
        "user_id": "12345"
    }

# Test case: missing token
def test_validate_token_missing():
    response = client.post("/validate_token")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Token not provided"
    }

# Test case: invalid token
@patch("main.auth.verify_id_token")
def test_validate_token_invalid(mock_verify):
    mock_verify.side_effect = Exception("Invalid token")

    headers = {
        "Authorization": "invalid_token_456"
    }

    with pytest.raises(Exception) as exc_info:
        client.post("/validate_token", headers=headers)

    assert str(exc_info.value) == "Invalid token"