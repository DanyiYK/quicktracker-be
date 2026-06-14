from flask import Blueprint, jsonify, request
from persistence.db_config import get_session
from service import package_service, delivery_service
from controller.auth_controller import token_required

delivery_bp = Blueprint("Delivery", __name__, url_prefix="/api")

@delivery_bp.route('/delivery', methods=["POST"])
def create_delivery():
    session = get_session()
    data = request.get_json()

    try:
        newPackage = package_service.create(session, data)
    except ValueError as e:
        return jsonify({"error": str(e)})
    
    try:
        newDelivery = delivery_service.create(session, data, newPackage.id)
    except ValueError as e:
        return jsonify({"error": str(e)})
    
    return jsonify(newDelivery.to_dict())