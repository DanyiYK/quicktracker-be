from sqlalchemy import select
from model.cap import Cap

def get_all(session):
    return session.execute(select(Cap)).scalars().all()

def get_by_cap(session, cap):
    return session.execute(
        select(Cap).filter_by(cap = cap)
    ).scalars().all()

def get_by_city(session, city_istat):
    return session.execute(
        select(Cap).filter_by(city_istat = city_istat)
    ).scalars().first()