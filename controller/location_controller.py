from flask import Blueprint, jsonify, request
from persistence.db_config import get_session
from service import courier_service
from controller.auth_controller import token_required
from service import region_service, province_service, city_service, cap_service
from controller.auth_controller import token_required

location_bp = Blueprint("location", __name__, url_prefix="/api/location")

@location_bp.route("/regions", methods=["GET"])
@token_required
def get_regions():
    session = get_session()

    region_list = region_service.get_all(session)

    session.close()

    return jsonify([region.to_dict() for region in region_list])

@location_bp.route("/region/<string:istat_code>", methods=["GET"])
@token_required
def get_region(istat_code):
    session = get_session()

    found = region_service.get_by_istat(session, istat_code)
    provinces = found and [province.to_dict() for province in found.provinces]

    session.close()

    if found is None:
        return jsonify({"error": "Region not found"}), 404
    
    found = found.to_dict()
    found["provinces"] = provinces

    return jsonify(found)


@location_bp.route("/region/<string:istat_code>/provinces", methods=["GET"])
@token_required
def get_provinces(istat_code):
    session = get_session()

    region = region_service.get_by_istat(session, istat_code)
    province_list = region and region.provinces

    session.close()

    if region is None:
        return jsonify({"error": "Region is not found!"}), 404

    return jsonify([province.to_dict() for province in province_list])

@location_bp.route("/province/<string:code>", methods=["GET"])
@token_required
def get_province(code):
    session = get_session()

    found = province_service.get_by_code(session, code)
    cities = found and [province.to_dict() for province in found.cities]

    session.close()

    if found is None:
        return jsonify({"error": "City not found"}), 404
    
    found = found.to_dict()
    found["cities"] = cities

    return jsonify(found)

@location_bp.route("/cities", methods=["GET"])
@token_required
def get_cities():
    session = get_session()

    cap = request.args.get("cap")
    
    if cap:
        found = cap_service.get_by_cap(session, cap)
        
        return_val = [data.city.to_dict() for data in found]
    else:
        found = city_service.get_all(session)

        return_val = [city.to_dict() for city in found]

    session.close()

    return jsonify(return_val)