from service import auth_service
from functools import wraps
from flask import Blueprint, g, jsonify, request
from persistence.db_config import get_session
from service import courier_service
from controller.auth_controller import token_required
import validator

courier_bp = Blueprint("courier", __name__, url_prefix="/api")

@courier_bp.route("/courier", methods=["POST"])
@token_required
def create_courier():
    data = request.get_json()
    session = get_session()

    try:
        new_courier = courier_service.create(session, data)

        return jsonify(new_courier.to_dict()), 201
    except ValueError as x:

        return jsonify({"error": f"{x}"}), 400
    finally:
        session.close()

@courier_bp.route("/courier/<int:courier_id>", methods=["PATCH"])
@token_required
def update_courier(courier_id):
    data = request.get_json()
    session = get_session()

    try:
        courier = courier_service.get_by_id(session, courier_id)

        if courier is None:
            return jsonify({"error": "Courier not found"}), 404

        courier_service.update(session, courier, data)

        return jsonify(courier.to_dict()), 201
    except ValueError as x:

        return jsonify({"error": f"{x}"}), 400
    finally:
        session.close()


@courier_bp.route("/couriers", methods=["GET"])
@token_required
def get_all_couriers():
    session = get_session()

    try:
        couriers = courier_service.get_all(session)

        return jsonify([courier.to_dict() for courier in couriers]), 200
    except Exception as x:
        print("ERROR:", x)

        return jsonify({"error": "There was an error while fetching data"}), 400
    finally:
        session.close()


@courier_bp.route("/courier/<int:courier_id>", methods=["GET"])
@token_required
def get_courier(courier_id):
    session = get_session()

    try:
        courier = courier_service.get_by_id(session, courier_id)

        if courier is None:
            return jsonify({"error": "Not found"}), 404

        return jsonify(courier.to_dict()), 200
    except ValueError as x:

        return jsonify({"error": f"{x}"}), 400
    finally:
        session.close()

@courier_bp.route("/courier/<int:courier_id>", methods=["DELETE"])
@token_required
def delete_courier(courier_id):
    session = get_session()

    try:
        courier = courier_service.get_by_id(session, courier_id)
    
        if courier is None:
            return jsonify({"error": "Not found"}), 404

        courier_service.delete(session, courier)

        return jsonify({"success": "courier was deleted"}), 200
    except ValueError as x:

        return jsonify({"error": f"{x}"}), 400
    finally:
        session.close()
