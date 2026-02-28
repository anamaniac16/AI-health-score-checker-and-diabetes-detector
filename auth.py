import json
import os
import hashlib

USERS_FILE = "users.json"
SESSION_FILE = "session.json"

# ---------- Ensure users file exists ----------
def initialize_storage():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

# ---------- Load Users ----------
def load_users():
    initialize_storage()
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# ---------- Save Users ----------
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------- Hash Password ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- Register User ----------
def register_user(email, password):
    users = load_users()

    if email in users:
        return False, "User already exists"

    users[email] = {
        "password": hash_password(password),
        "history": [],
        "primary": False
    }

    # First user becomes primary
    if len(users) == 1:
        users[email]["primary"] = True

    save_users(users)
    return True, "User registered successfully"

# ---------- Login User ----------
def login_user(email, password):
    users = load_users()

    if email not in users:
        return False, "User not found"

    if users[email]["password"] != hash_password(password):
        return False, "Incorrect password"

    return True, "Login successful"

# ---------- Add Health Record ----------
def add_health_record(email, record):
    users = load_users()

    users[email]["history"].append(record)
    save_users(users)

# ---------- Get User History ----------
def get_user_history(email):
    users = load_users()
    return users[email]["history"]

# ---------- Save Session ----------
def save_session(email):
    with open(SESSION_FILE, "w") as f:
        json.dump({"current_user": email}, f)

# ---------- Load Session ----------
def load_session():
    if not os.path.exists(SESSION_FILE):
        return None

    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("current_user")

# ---------- Clear Session ----------
def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)