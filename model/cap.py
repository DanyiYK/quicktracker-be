from sqlalchemy import event, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped
from persistence.db_config import Base
import json

class Cap(Base):
    __tablename__ = "cap"

    cap = Column(String(5), primary_key=True)
    city_istat = Column(ForeignKey("city.istat_code"), primary_key=True)

    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)

    city = relationship("City", back_populates="caps")

    def to_dict(self):
        return {
            "istat_code": self.istat_code,
            "province_istat": self.province_istat,
            "name": self.name,
        }

    def __repr__(self):
        return f"City(istat_code={self.istat_code}, name={self.name}, province_istat={self.province_istat})"

    def __eq__(self, other):
        if not isinstance(other, City):
            return False

        return self.istat_code==other.istat_code

@event.listens_for(Cap.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    print("Adding default cap data...")

    with open("data/caps.json") as file:
        content = file.read()
    
    data = json.loads(content)

    connection.execute(
        Cap.__table__.insert(),
        [
            {
                "cap": cap[0],
                "city_istat": cap[1],
                "lat": cap[2],
                "long": cap[3]
            }
            for cap in data
        ]
    )