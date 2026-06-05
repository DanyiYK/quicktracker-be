from service import auth_service
from functools import wraps
from flask import Blueprint, g, jsonify, request
from persistence.db_config import get_session

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    session = get_session()

    try:
        token, username = auth_service.login(session, data)

        return jsonify({"token": token, "username": username}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
    finally:
        session.close()

def token_required(f):
    @wraps
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth_data = request.headers["Authorization"].split(" ")
            if len(auth_data)==2 and auth_data[0]=="Bearer":
                token = auth_data[1]
            else:
                return jsonify({"error": "Auth token is required!"}), 401

            try:
                payload = auth_service.check_token(token)

                g.admin_id = payload["admin_id"]
                g.admin_email = payload["admin_email"]
            except ValueError as e:
                return jsonify({"error": str(e)}), 401
            
        return f(*args, **kwargs)

    return decorated

@token_required
@auth_bp.route("/me", methods=["GET"])
def me():
    session = get_session()
    
    return auth_service.me(session, g.admin_id)