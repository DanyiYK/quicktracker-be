from service import auth_service
from functools import wraps
from flask import Blueprint, g, jsonify, request
from persistence.db_config import get_session

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.get_json()
    session = get_session()

    try:
        token, name, surname = auth_service.login(session, data)
        session.close()

        return jsonify({"token": token, "name": name, "surname": surname}), 200
    except ValueError as e:
        session.close()

        return jsonify({"error": str(e)}), 401

def token_required(f):
    @wraps(f)
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
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": "Token is missing"}), 401

        return f(*args, **kwargs)

    return decorated

@auth_bp.route("/me", methods=["GET"])
@token_required
def me():
    session = get_session()
    admin = auth_service.me(session, g.admin_id)

    session.close()

    if admin is None:
        return jsonify({"error": "Account not found"}), 404
    
    return admin