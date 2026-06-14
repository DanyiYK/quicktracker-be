from service import auth_service
from model.package import Package
from repository import package_repository
import validator

def get_all(session):
    return package_repository.get_all(session)

def get_by_id(session, package_id):
    return package_repository.get_by_id(session, package_id)

def create(session, data):
    for field in ["content", "weight", "size"]:
        if field not in data:
            raise ValueError(f'Field "{field}" is required')
    
    content:str = str(data["content"]).strip()

    if not validator.check_string(content):
        raise ValueError("Content cannot be empty")

    weight = data["weight"]
    
    try:
        weight = float(weight)
    except ValueError:
        raise ValueError("Weight must be a number!")
    
    if not validator.check_weight(weight):
        raise ValueError("Weight must be a number between 0 and 500!")

    size = data["size"]

    if not validator.check_size(size):
        raise ValueError("Invalid size!")

    fragile = bool(data.get("fragile")) # No need to check this value, it will always be a bool

    newPackage = Package(
        content = content,
        weight = weight,
        size = size,
        is_fragile = fragile
    )

    return package_repository.create(session, newPackage)