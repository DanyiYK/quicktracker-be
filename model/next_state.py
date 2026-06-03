from sqlalchemy import event, Column, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped
from persistence.db_config import Base
import json


class NextState(Base):
    __tablename__ = "next_state"

    id = Column(ForeignKey("state.id"), primary_key=True)
    next_state_id = Column(ForeignKey("state.id"), primary_key=True)
    
    next_state = relationship("State", foreign_keys=[next_state_id])
    
    def to_dict(self):
        return {
            "id": self.id,
            "next_state_id": self.next_state_id,
        }

    def __repr__(self):
        return f"State(id={self.id}, next_state_id={self.next_state_id})"

    def __eq__(self, other):
        if not isinstance(other, NextState):
            return False

        return self.id==other.id

@event.listens_for(NextState.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    print("Adding next states data...")
    
    with open("data/states.json") as file:
        content = file.read()
    
    found_data = json.loads(content)

    to_add = []

    for data in found_data:
        for next_state in data["next_states"]:
            to_add.append({
                "id": data["id"],
                "next_state_id": next_state
            })

    connection.execute(
        NextState.__table__.insert(),
        to_add
    )
