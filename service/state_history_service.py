from service import delivery_service, delivery_state_service
from model.delivery_state_history import DeliveryStateHistory
from repository import state_history_repository

def get_all(session):
    return state_history_repository.get_all(session)

def get_by_id(session, id):
    return state_history_repository.get_by_id(session, id)

def get_by_delivery(session, tracking_code):
    return state_history_repository.get_by_delivery(session, tracking_code)

def get_states_after(session, statehistory_id):
    found = get_by_id(statehistory_id)

    if not found:
        raise ValueError("State history does not exist!")

    return state_history_repository.get_states_after(session, statehistory_id)

def create(session, data):
    for field in ["delivery_id", "state_id"]:
        if field not in data:
            raise ValueError(f'Field "{field}" is missing!')
    
    delivery_id = data["delivery_id"]

    if delivery_service.get_by_id(session, delivery_id) is None:
        raise ValueError("Delivery not found")
    
    state_id = data["state_id"]

    if delivery_state_service.get_by_id(session, state_id) is None:
        raise ValueError("Delivery state not found")
    
    new = state_history_repository.create(session, DeliveryStateHistory(
        delivery_id = delivery_id,
        state_id = state_id
    ))

    return state_history_repository.create(session, new)

def delete(session, statehistory):
    return state_history_repository.delete(session, statehistory)

def update(session, statehistory):
    return state_history_repository.update(session, statehistory)