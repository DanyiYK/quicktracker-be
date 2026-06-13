from service import auth_service
from model.region import Region
from repository import region_repository

def get_all(session):
    return region_repository.get_all(session)

def get_by_istat(session, istat):
    return region_repository.get_by_istat(session, istat)