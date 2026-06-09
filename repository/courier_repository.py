from sqlalchemy import select
from model.courier import Courier

def get_all(session):
    return session.execute(select(Courier)).scalars().all()

def get_by_id(session, courier_id):
    return session.get(Courier, courier_id)

def get_by_fiscal_code(session, fiscal_code):
    return session.execute(
        select(Courier).filter_by(fiscal_code = fiscal_code)
    ).scalars().first()

def get_by_email(session, email):
    return session.execute(
        select(Courier).filter_by(email = email)
    ).scalars().first()

def create(session, courier):
    session.add(courier)
    session.commit()
    return courier

def delete_by_id(session, courier):
    session.delete(courier)
    session.commit()

def update(session, courier):
    session.commit()
    return courier