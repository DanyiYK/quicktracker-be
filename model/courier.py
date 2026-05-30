from sqlalchemy import Column, Integer, String

from persistence.db_config import Base


class Courier(Base):
    __tablename__ = "courier"

    fiscal_code = Column(String(16), primary_key=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)

    # Contacts
    email = Column(String(150), unique=True, nullable=True)
    phone_number = Column(String(32), unique=True, nullable=False)

    def to_dict(self):
        return {
            "fiscal_code": self.fiscal_code,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "phone_number": self.phone_number
        }

    def __repr__(self):
        return f"Courier(id={self.id}, name={self.name}, surname={self.surname}, email={self.email}, phone_number={self.phone_number})"

    def __eq__(self, other):
        if not isinstance(other, Courier):
            return False

        return self.fiscal_code==other.fiscal_code