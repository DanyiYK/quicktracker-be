from sqlalchemy import Column, Integer, String

from persistence.db_config import Base


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(200), nullable=False) # Password hash

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
        }

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

    def __eq__(self, other):
        if not isinstance(other, Admin):
            return False

        return self.id==other.id