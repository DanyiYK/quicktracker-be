from sqlalchemy import select
from model.delivery_state import DeliveryState

def get_all(session):
    return session.execute(select(DeliveryState)).scalars().all()

def get_by_id(session, id):
    return session.get(DeliveryState, id)

def get_by_name(session, name):
    return session.execute(
        select(DeliveryState).filter_by( display_name=name )
    ).scalars().first()