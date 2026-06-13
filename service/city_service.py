from service import auth_service
from model.courier import Courier
from repository import city_repository

def get_all(session):
    return city_repository.get_all(session)

def get_by_istat(session, istat):
    return city_repository.get_by_istat(session, istat)