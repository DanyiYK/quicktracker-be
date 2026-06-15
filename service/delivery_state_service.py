from model.delivery_state import DeliveryState
from repository import delivery_state_repository

def get_all(session):
    return delivery_state_repository.get_all(session)

def get_by_id(session, id):
    return delivery_state_repository.get_by_id(session, id)

def get_by_name(session, name):
    return delivery_state_repository.get_by_name(session, name)