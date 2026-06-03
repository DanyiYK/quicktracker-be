from sqlalchemy import event, Column, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped
from persistence.db_config import Base
import json


class NextDeliveryState(Base):
    __tablename__ = "next_delivery_state"

    id = Column(ForeignKey("delivery_state.id"), primary_key=True)
    next_delivery_state_id = Column(ForeignKey("delivery_state.id"), primary_key=True)
    
    next_delivery_state = relationship("DeliveryState", foreign_keys=[next_delivery_state_id])
    
    def to_dict(self):
        return {
            "id": self.id,
            "next_state_id": self.next_delivery_state_id,
        }

    def __repr__(self):
        return f"State(id={self.id}, next_state_id={self.next_delivery_state_id})"

    def __eq__(self, other):
        if not isinstance(other, NextDeliveryState):
            return False

        return self.id==other.id

@event.listens_for(NextDeliveryState.__table__, 'after_create')
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
        NextDeliveryState.__table__.insert(),
        to_add
    )
