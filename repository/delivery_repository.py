from sqlalchemy import select
from model.delivery import Delivery

def get_all(session):
    return session.execute(select(Delivery)).scalars().all()

def get_by_id(session, delivery_id):
    return session.get(Delivery, delivery_id)

def get_by_tracking_code(session, tracking_code):
    return session.execute(
        select(Delivery).filter_by(tracking_code = tracking_code)
    )

def create(session, delivery):
    session.add(delivery)
    session.commit()
    return delivery

def delete(session, delivery):
    session.delete(delivery)
    session.commit()

def update(session, delivery):
    session.commit()
    return delivery