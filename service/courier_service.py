from service import auth_service
from functools import wraps
from flask import Blueprint, g, jsonify, request
from persistence.db_config import get_session
from model.courier import Courier
from repository import courier_repository
import validator

def create(session, data):
    for field in ["name", "surname", "fiscal_code", "phone_number", "email"]:
        if field not in data:
            raise ValueError(f"Field \"{field}\" is missing!")
        else:
            data[field] = data[field].strip()
    
    name = data["name"]
    surname = data["surname"]
    fiscal_code = data["fiscal_code"]
    email = data["email"]
    phone_number = data["phone_number"]

    if not validator.check_name(name):
        raise ValueError("Invalid name")
    
    if not validator.check_name(surname):
        raise ValueError("Invalid surname")
    
    if not validator.check_fiscal_code(fiscal_code):
        raise ValueError("Invalid fiscal code")

    if not validator.check_email(email):
        raise ValueError("Invalid email")

    if not validator.check_phone_number(phone_number):
        raise ValueError("Invalid phone number")
    
    if courier_repository.get_by_fiscal_code(session, fiscal_code) is not None:
        raise ValueError("A courier with this fiscal code already exists!")

    new_courier = Courier(
        name = name,
        surname = surname,
        fiscal_code = fiscal_code,
        phone_number = phone_number,
        email = email
    )

    return courier_repository.create(session, new_courier)

def get_by_id(session, courier_id):
    return courier_repository.get_by_id(session, courier_id)

def get_all(session):
    return courier_repository.get_all(session)