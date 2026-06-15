from sqlalchemy import select
from model.delivery_state_history import DeliveryStateHistory

def get_all(session):
    return session.execute(select(DeliveryStateHistory)).scalars().all()

def get_by_id(session, id):
    return session.get(DeliveryStateHistory, id)

def get_by_delivery(session, tracking_code):
    return session.execute(
        select(DeliveryStateHistory).filter_by(tracking_code = tracking_code).order_by()
    ).scalars().all()

def get_states_after(session, statehistory):
    return session.execute(
        select(DeliveryStateHistory).filter(
            DeliveryStateHistory.creation_date > statehistory.creation_date,
            DeliveryStateHistory.tracking_code == statehistory.tracking_code
        )
    ).scalars().all()

def create(session, statehistory):
    session.add(statehistory)
    session.commit()
    return statehistory

def delete(session, statehistory):
    session.delete(statehistory)
    session.commit()

def update(session, statehistory):
    session.commit()
    return statehistory