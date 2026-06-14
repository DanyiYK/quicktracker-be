from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

class Base(DeclarativeBase):
    pass

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
URL = os.getenv("DB_URL")
DATABASE_NAME = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{URL}/{DATABASE_NAME}")

SessionLocal = sessionmaker(bind=engine)


def init_db():
    import model.admin
    import model.courier
    import model.region
    import model.province
    import model.city
    import model.cap
    import model.delivery_state
    import model.next_delivery_state
    import model.package
    import model.delivery

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()