from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

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
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()