from sqlalchemy import Column, Integer, String, Float, Boolean

from persistence.db_config import Base


class Package(Base):
    __tablename__ = "package"

    id = Column(Integer, autoincrement=True, primary_key=True)
    content = Column(String(500), nullable=False)
    is_fragile = Column(Boolean, nullable=False, default=False)
    weight = Column(Float, nullable=False) # Kg
    size = Column(String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "is_fragile": self.is_fragile,
            "weight": self.weight,
            "size": self.size,
        }

    def __repr__(self):
        return f"Package(id={self.id}, is_fragile={self.is_fragile}, weight={self.weight}, base={self.base}, height={self.height}, depth={self.depth})"

    def __eq__(self, other):
        if not isinstance(other, Package):
            return False

        return self.id==other.id