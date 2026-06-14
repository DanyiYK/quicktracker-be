from sqlalchemy import event, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped
from persistence.db_config import Base
import json

class Cap(Base):
    __tablename__ = "cap"

    id = Column(Integer, primary_key=True)

    cap = Column(String(5))
    city_istat = Column(ForeignKey("city.istat_code"))

    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)

    city = relationship("City", back_populates="caps")

    def to_dict(self):
        return {
            "cap": self.cap,
            "city_istat": self.city_istat,
            "lat": self.lat,
            "long": self.long,
        }

    def __repr__(self):
        return f"Cap(cap={self.cap}, city_istat={self.city_istat}, lat={self.lat}, long={self.long})"

    def __eq__(self, other):
        if not isinstance(other, Cap):
            return False

        return self.cap==other.cap and self.city_istat==self.city_istat

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