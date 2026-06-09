from sqlalchemy import event, Column, Integer, String, Boolean
from persistence.db_config import Base
import json


class State(Base):
    __tablename__ = "state"

    id = Column(Integer, primary_key=True)
    display_name = Column(String(100), nullable=False)
    is_final_state = Column(Boolean(), default=False, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "display_name": self.display_name,
            "is_final_state": self.is_final_state,
        }

    def __repr__(self):
        return f"State(id={self.id}, display_name={self.display_name}, is_final_state={self.is_final_state})"

    def __eq__(self, other):
        if not isinstance(other, State):
            return False

        return self.id==other.id

@event.listens_for(State.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    print("Adding default region data...")
    
    with open("data/regions.json") as file:
        content = file.read()
    
    data = json.loads(content)

    connection.execute(
        State.__table__.insert(),
        [
            {
                "cod_istat": region["cod_istat"],
                "name": region["name"],
            }
            for region in data
        ]
    )
