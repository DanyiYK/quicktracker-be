from flask import Blueprint, jsonify, request
from persistence.db_config import get_session
from service import package_service, delivery_service
from controller.auth_controller import token_required

delivery_bp = Blueprint("Delivery", __name__, url_prefix="/api")

@delivery_bp.route('/delivery', methods=["POST"])
@token_required
def create_delivery():
    session = get_session()
    data = request.get_json()

    try:
        newPackage = package_service.create(session, data)
    except ValueError as e:
        session.close()
        return jsonify({"error": str(e)})

    try:
        newDelivery = delivery_service.create(session, data, newPackage.id)
    except ValueError as e:
        session.close()
        return jsonify({"error": str(e)})
    
    return_val = newDelivery.to_dict()
    session.close()

    return jsonify(return_val)

@delivery_bp.route("/deliveries", methods=["GET"])
@token_required
def get_deliveries():
    session = get_session()
    deliveries = delivery_service.get_all(session)
    
    return_val = [
    {
        "tracking_code": d.tracking_code,
        "creation_date": d.creation_date,
        "is_closed": d.is_closed,
        "courier": {"id": d.courier.id, "name": f"{d.courier.name} {d.courier.surname}"}
    }
    for d in deliveries]

    session.close()

    return jsonify(return_val)

@delivery_bp.route("/delivery/<int:id>")
@token_required
def get_delivery(id):
    session = get_session()
    found = delivery_service.get_by_id(session, id)

    if not found:
        session.close()
        return jsonify({"error": "Not found"}), 404
    
    return_val = found.to_dict()

    session.close()

    return jsonify(return_val)