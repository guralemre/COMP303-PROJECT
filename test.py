import requests

BASE_URL = "http://127.0.0.1:5000/api"  # Flask uygulamanızın temel URL'si

def test_signup():
    print("Testing signup...")
    payload = {
        "username": "emre123",
        "email": "admin@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/signup", json=payload)
    print(f"Signup Response: {response.status_code}, {response.json()}\n")

def test_login(new_password=False):
    print("Testing login...")
    payload = {
        "username": "emre123",
        "password": "testpassword123" if new_password else "newtestpassword123"
    }
    response = requests.post(f"{BASE_URL}/login", json=payload)
    print(f"Login Response: {response.status_code}, {response.json()}\n")
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Access Token: {token}")
        return token
    return None

def test_password_reset():
    print("Testing password reset...")
    payload = {
        "email": "admin@example.com",
        "password": "newtestpassword123"
    }
    response = requests.post(f"{BASE_URL}/reset", json=payload)
    print(f"Password Reset Response: {response.status_code}, {response.json()}\n")

def test_protected_route(token):
    print("Testing protected route...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print(f"Protected Route Response: {response.status_code}, {response.json()}\n")

if __name__ == "__main__":
    # 1. Kayıt olmayı test et
    test_signup()

    # 2. Giriş yapmayı test et
    token = test_login()

    # 3. Token ile korumalı bir rota test et
    if token:
        test_protected_route(token)

    # 4. Şifre sıfırlamayı test et
    test_password_reset()
    # 5. Yeni şifre ile giriş yapmayı test et
    token = test_login()
    if token:
        test_protected_route(token)
