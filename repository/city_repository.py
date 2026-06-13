from sqlalchemy import select
from model.city import City

def get_all(session):
    return session.execute(select(City).order_by(City.name)).scalars().all()

def get_by_province(session, province_istat):
    return session.execute(
        select(City).filter_by(province_istat = province_istat)
    ).scalars().all()

def get_by_istat(session, istat):
    return session.execute(
        select(City).filter_by(cod_istat = istat)
    ).scalars().first()