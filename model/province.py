from sqlalchemy import event, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, sessionmaker
from persistence.db_config import Base
import json

class Province(Base):
    __tablename__ = "province"

    cod_istat = Column(String(3), primary_key=True)
    region_istat = Column(ForeignKey("region.cod_istat"))
    name = Column(String(100), nullable=False)

    region = relationship("Region", back_populates="provinces")
    cities = relationship("City", back_populates="province")

    def to_dict(self):
        return {
            "cod_istat": self.cod_istat,
            "region_istat": self.region_istat,
            "name": self.name,
        }

    def __repr__(self):
        return f"Province(cod_istat={self.cod_istat}, name={self.name})"

    def __eq__(self, other):
        if not isinstance(other, Province):
            return False

        return self.cod_istat==other.cod_istat

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
                "cod_istat": province["cod_istat"],
                "region_istat": province["region_istat"],
                "name": province["name"],
            }
            for province in data
        ]
    )