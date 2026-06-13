from service import auth_service
from model.courier import Courier
from repository import province_repository

def get_all(session):
    return province_repository.get_all(session)


def get_by_region(session, region_istat):
    return province_repository.get_by_region(session, region_istat)

def get_by_code(session, code):
    return province_repository.get_by_code(session, code)