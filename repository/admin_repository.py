from sqlalchemy import select
from model.admin import Admin

def get_all(session):
    return session.execute(select(Admin)).scalars().all()

def get_by_id(session, admin_id):
    return session.get(Admin, admin_id)

def get_by_username(session, username):
    return session.execute(
        select(Admin).filter_by(username = username)
    ).scalars().first()

def get_by_email(session, email):
    return session.execute(
        select(Admin).filter_by(email = email)
    ).scalars().first()

def create(session, admin):
    session.add(admin)
    session.commit()
    return admin

def delete_by_id(session, admin):
    session.delete(admin)
    session.commit()

def update(session, admin):
    session.commit()
    return admin