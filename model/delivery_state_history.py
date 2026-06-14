from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime

from persistence.db_config import Base


class DeliveryStateHistory(Base):
    __tablename__ = "delivery"

    id = Column(Integer, autoincrement=True, primary_key=True)
    delivery_code = Column(ForeignKey("delivery.id"), nullable=False)
    state_id = Column(ForeignKey("delivary_state.id"), nullable=False)
    timestamp = Column(DateTime(), nullable=False)

    def to_dict(self):
        # TODO: Finish this dict
        return {
        }

    def __repr__(self):
        return f"DeliveryStateHistory()"

    def __eq__(self, other):
        if not isinstance(other, DeliveryStateHistory):
            return False

        return self.id==other.id