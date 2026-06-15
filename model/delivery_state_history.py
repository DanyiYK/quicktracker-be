from sqlalchemy import Column, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import relationship

from persistence.db_config import Base


class DeliveryStateHistory(Base):
    __tablename__ = "delivery_state_history"

    id = Column(Integer, autoincrement=True, primary_key=True)
    delivery_id = Column(ForeignKey("delivery.id"), nullable=False)
    state_id = Column(ForeignKey("delivery_state.id"), nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    state = relationship("DeliveryState", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            # "state_id": self.state_id,
            "delivery_id": self.delivery_id,
            "display_name": self.state.display_name,
            "datetime": self.datetime,
            "state": self.state.to_dict()
        }

    def __repr__(self):
        return f"DeliveryStateHistory()"

    def __eq__(self, other):
        if not isinstance(other, DeliveryStateHistory):
            return False

        return self.id==other.id