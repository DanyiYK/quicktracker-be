from sqlalchemy import select
from model.package import Package

def get_all(session):
    return session.execute(select(Package)).scalars().all()

def get_by_id(session, package_id):
    return session.get(Package, package_id)

def create(session, package):
    session.add(package)
    session.commit()
    return package

def delete_by_id(session, package):
    session.delete(package)
    session.commit()

def update(session, package):
    session.commit()
    return package