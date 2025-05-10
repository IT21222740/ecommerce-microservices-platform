import unittest
from fastapi.testclient import TestClient
from grpc import Status
import pytest
from main import app
from unittest.mock import patch 
from unittest.mock import MagicMock
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


class TestAuthRoutes(unittest.TestCase):

    @patch("routes.auth.auth.create_user")
    def test_signup_success(self, mock_create_user):
        mock_create_user.return_value = MagicMock(uid="fake-uid-123")

        response = client.post("/SignUp", json={
            "email": "test@example.com",
            "password": "securepassword"
        })

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            "message": "User created successfully",
            "user_id": "fake-uid-123"
        })
        mock_create_user.assert_called_once()

    @patch("routes.auth.firebase")
    def test_signin_success(self, mock_firebase):
        # Mock the result of firebase.auth()
        mock_auth_instance = MagicMock()
        mock_auth_instance.sign_in_with_email_and_password.return_value = {
            "idToken": "mocked-id-token"
        }
        mock_firebase.auth.return_value = mock_auth_instance

        response = client.post("/SignIn", json={
            "email": "user@example.com",
            "password": "password123"
        })

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json(), {
            "message": "User signed in successfully",
            "token": "mocked-id-token"
        })


    @patch("routes.auth.firebase")
    def test_signin_invalid_credentials(self, mock_firebase):
        mock_auth_instance = MagicMock()
        mock_auth_instance.sign_in_with_email_and_password.side_effect = Exception("Auth error")
        mock_firebase.auth.return_value = mock_auth_instance

        response = client.post("/SignIn", json={
            "email": "wrong@example.com",
            "password": "wrongpass"
        })

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid credentials", response.text)



    ##test cases for /set role

@patch("routes.profile.auth")
def test_set_role_success(mock_auth):
    response = client.post("/set_role", json={
        "uid": "test-user-uid",
        "role": "admin"
    })
    mock_auth.set_custom_user_claims.assert_called_once_with("test-user-uid", {"role": "admin"})
    assert response.status_code == 200
    assert response.json() == {"message": "Role 'admin' has been set for user test-user-uid"}    

#test case for edit_profile 

@patch("routes.profile.auth")
def test_edit_profile_success(mock_auth):
    # Mock token verification
    mock_auth.verify_id_token.return_value = {"uid": "user123"}

    response = client.put("/edit_profile", json={
        "full_name": "John Doe",
        "phone_number": "+123456789"
    }, headers={"Authorization": "Bearer fake-token"})

    mock_auth.verify_id_token.assert_called_once_with("fake-token")
    mock_auth.update_user.assert_called_once_with("user123", display_name="John Doe", phone_number="+123456789")

    assert response.status_code == 200
    assert response.json()["message"] == "Profile updated successfully"

@patch("routes.profile.auth")
def test_edit_profile_server_error(mock_auth):
    mock_auth.verify_id_token.side_effect = Exception("Bad token")

    response = client.put("/edit_profile", json={
        "full_name": "Jane"
    }, headers={"Authorization": "Bearer bad-token"})

    assert response.status_code == 500
    assert "Bad token" in response.json()["detail"]    

if __name__ == "__main__":
    pytest.main()