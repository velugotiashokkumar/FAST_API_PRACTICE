from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user/read-user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "ruby1234"
    assert response.json()["email"] == "ruby@gmail.com"
    assert response.json()["first_name"] == "ruby"
    assert response.json()["last_name"] == "joe"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "1234567890"
    
def test_change_password_success(test_user):
    response = client.put("/user/update-password", json={"password": "pass1234", "new_password": "pass123456"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/update-password", json={"password": "pass", "new_password": "pass123456"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "The present Password is invalid"}
    
def test_change_phone_number_success(test_user):
    response = client.put("/user/update-phone-number/?new_phone_number=0987654321")
    assert response.status_code == status.HTTP_204_NO_CONTENT