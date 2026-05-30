from sqlalchemy import Column, Integer, String, Float, Boolean

from persistence.db_config import Base


class Package(Base):
    __tablename__ = "package"

    id = Column(Integer, autoincrement=True, primary_key=True)
    recipient = Column(String(100), nullable=False) # The name of the entity that should receive the package
    is_fragile = Column(Boolean, nullable=False, default=False)

    # Measurements (used to retrieve the cost of the delivery)
    weight = Column(Float, nullable=False) # Kg
    base = Column(Float, nullable=True) # m metres
    height = Column(Float, nullable=False) # metres
    depth = Column(Float, nullable=False) # meters

    def to_dict(self):
        return {
            "id": self.id,
            "recipient": self.recipient,
            "is_fragile": self.is_fragile,
            "weight": self.weight,
            "base": self.base,
            "height": self.height,
            "depth": self.depth,
        }

    def __repr__(self):
        return f"Package(id={self.id}, is_fragile={self.is_fragile}, weight={self.weight}, base={self.base}, height={self.height}, depth={self.depth})"

    def __eq__(self, other):
        if not isinstance(other, Package):
            return False

        return self.id==other.id