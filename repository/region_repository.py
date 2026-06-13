from sqlalchemy import select
from model.region import Region
from model.province import Province

def get_all(session):
    return session.execute(select(Region)).scalars().all()

def get_by_istat(session, istat):
    return session.execute(
        select(Region).filter_by(istat_code = istat)
    ).scalars().first()