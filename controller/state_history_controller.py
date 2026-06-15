from flask import Blueprint, jsonify, request
from persistence.db_config import get_session
from service import state_history_service
from controller.auth_controller import token_required

state_history_bp = Blueprint("StateHistory", __name__, url_prefix="/api")

@state_history_bp.route('/history', methods=["POST"])
@token_required
def create_delivery():
    session = get_session()
    data = request.get_json()

    try:
        newStateHistory = state_history_service.create(session, data)
    except ValueError as e:
        session.close()
        return jsonify({"error": str(e)})
    
    return jsonify(newStateHistory.to_dict())