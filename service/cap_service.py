from service import auth_service
from model.courier import Courier
from repository import cap_repository

def get_all(session):
    return cap_repository.get_all(session)

def get_by_cap(session, cap):
    return cap_repository.get_by_cap(session, cap)

def get_by_city(session, city_istat):
    return cap_repository.get_by_city(session, city_istat=city_istat)

def get_by_city_and_cap(session, city_istat, cap):
    return cap_repository.get_by_city_and_cap(session, city_istat, cap)