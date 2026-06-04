import repository.admin_repository as admin_repository
from model.admin import Admin
import datetime
import bcrypt
import jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET")

# Admins cannot be registered from the front-end
# This function isn't used in any route
def register(session, data):
    for field in ["name", "surname", "email", "password"]:
        if field not in data or len(str(data[field]).strip()) == 0:
            raise ValueError(f'Field "{field}" is missing!')
        
    if len(data["password"])<4:
        raise ValueError("Password is too short! (at least 4 characters)")
    elif len(data["password"]>=128):
        raise ValueError("Password is too long! (password length cannot exceed 128 characters)")

    if admin_repository.get_by_email(data["email"]):
        raise ValueError("An admin with this email already exists")
        
    password_hash = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    new_admin = Admin(
        name=data["name"],
        surname=data["surname"],
        email=data["email"],
        password=data["password"]
    )

    return admin_repository.create(session, new_admin)
        
def login(session, data):
    if "email" not in data or "password" not in data:
        raise ValueError("Email or password missing")

    admin = admin_repository.get_by_email(session, data["email"])

    if admin is None:
        return ValueError("Invalid credentials!")

    is_password_valid = bcrypt.checkpw(
        data["password"].encode("utf-8"),
        admin.password.encode("utf-8")
    )
    
    if not is_password_valid:
        return ValueError("Invalid credentials!")

    payload = {
        "admin_id": admin.id,
        "admin_email": admin.email,
        "admin_username": admin.username,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token, admin.username

def me(session, admin_id):
    return admin_repository.get_by_id(session, admin_id)

def check_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Expired token")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")