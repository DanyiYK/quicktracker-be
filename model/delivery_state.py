from typing import List
from sqlalchemy import event, Column, Boolean, String, Integer
from sqlalchemy.orm import relationship, Mapped
from persistence.db_config import Base
import json

from model.next_delivery_state import NextDeliveryState

class DeliveryState(Base):
    __tablename__ = "delivery_state"

    id = Column(Integer, primary_key=True)
    display_name = Column(String(100), nullable=False)
    is_final_state = Column(Boolean, nullable=False)

    next_states: Mapped[List["NextDeliveryState"]] = relationship(foreign_keys=[NextDeliveryState.id])

    def to_dict(self):
        return {
            "id": self.id,
            "display_name": self.display_name,
            "is_final_state": self.is_final_state,
            "next_states": [{"id": state.state.id, "display_name": state.state.display_name} for state in self.next_states]
        }

    def __repr__(self):
        return f"DeliveryState(id={self.id}, display_name={self.display_name}, is_final_state={self.is_final_state})"

    def __eq__(self, other):
        if not isinstance(other, DeliveryState):
            return False

        return self.id==other.id

@event.listens_for(DeliveryState.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    print("Adding delivery state data...")
    
    with open("data/delivery_states.json") as file:
        content = file.read()
    
    found_data = json.loads(content)

    connection.execute(
        DeliveryState.__table__.insert(),
        [
            {
                "id": data["id"],
                "display_name": data["display_name"],
                "is_final_state": data["is_final_state"]
            }
            for data in found_data
        ]
    )