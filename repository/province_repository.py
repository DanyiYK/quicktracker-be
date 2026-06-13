from sqlalchemy import select
from model.province import Province

def get_all(session):
    return session.execute(select(City).order_by(Province.name)).scalars().all()

def get_by_region(session, region_istat):
    return session.execute(
        select(Province).filter_by(region_istat=region_istat)
    ).scalars().all()

def get_by_code(session, code):
    return session.execute(
        select(Province).filter_by(code = code)
    ).scalars().first()