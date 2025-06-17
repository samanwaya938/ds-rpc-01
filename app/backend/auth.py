# backend/auth.py

users_db = {
    "alice": {"password": "1234", "role": "engineering"},
    "bob": {"password": "abcd", "role": "hr"},
    "charlie": {"password": "xyz", "role": "finance"},
}

def authenticate_user(username: str, password: str, role: str) -> bool:
    user = users_db.get(username)
    return user and user["password"] == password and user["role"] == role


