from sqlalchemy import event, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, sessionmaker
from persistence.db_config import Base
import json

class Province(Base):
    __tablename__ = "province"

    code = Column(String(3), primary_key=True)
    region_istat = Column(ForeignKey("region.istat_code"))
    name = Column(String(100), nullable=False)

    region = relationship("Region", back_populates="provinces")
    cities = relationship("City", back_populates="province", order_by="asc(City.name)")

    def to_dict(self):
        return {
            "code": self.code,
            "region_istat": self.region_istat,
            "name": self.name,
        }

    def __repr__(self):
        return f"Province(code={self.code}, region_istat={self.region_istat}, name={self.name})"

    def __eq__(self, other):
        if not isinstance(other, Province):
            return False

        return self.code==other.code

@event.listens_for(Province.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    print("Adding default province data...")

    with open("data/provinces.json") as file:
        content = file.read()
    
    data = json.loads(content)

    connection.execute(
        Province.__table__.insert(),
        [
            {
                "code": province[0],
                "region_istat": province[1],
                "name": province[2],
            }
            for province in data
        ]
    )