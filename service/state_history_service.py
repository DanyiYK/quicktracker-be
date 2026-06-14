from service import auth_service
from model.package import Package
from repository import state_history_repository
import validator

def get_all(session):
    return state_history_repository.get_all()

def get_by_id(session, id):
    return state_history_repository.get_by_id(session, id)

def get_by_delivery(session, tracking_code):
    return state_history_repository.get_by_delivery(session, tracking_code)

def get_states_after(session, statehistory_id):
    found = get_by_id(statehistory_id)

    if not found:
        raise ValueError("State history does not exist!")

    return state_history_repository.get_states_after(session, statehistory_id)

def create(session, statehistory):
    return state_history_repository.create(session, statehistory)

def delete(session, statehistory):
    return state_history_repository.delete(session, statehistory)

def update(session, statehistory):
    return state_history_repository.update(session, statehistory)