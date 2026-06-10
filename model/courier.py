from sqlalchemy import event, Column, Integer, String

from persistence.db_config import Base
import json

class Courier(Base):
    __tablename__ = "courier"

    id = Column(Integer, autoincrement=True, primary_key=True)
    fiscal_code = Column(String(16), unique=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)

    # Contacts
    email = Column(String(150), unique=True, nullable=True)
    phone_number = Column(String(32), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
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
    
@event.listens_for(Courier.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    print("Adding default courier data...")
    
    with open("data/couriers.json") as file:
        content = file.read()
    
    data = json.loads(content)

    connection.execute(
        Courier.__table__.insert(),
        [
            {
                "id": courier["id"],
                "name": courier["name"],
                "surname": courier["surname"],
                "fiscal_code": courier["fiscal_code"],
                "phone_number": courier["phone_number"],
                "email": courier["email"]
            }
            for courier in data
        ]
    )
