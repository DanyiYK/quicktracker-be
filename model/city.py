from sqlalchemy import event, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped
from persistence.db_config import Base
import json

class City(Base):
    __tablename__ = "city"

    istat_code = Column(String(6), primary_key=True)
    province_code = Column(ForeignKey("province.code"))
    name = Column(String(100), nullable=False)

    province = relationship("Province", back_populates="cities")
    caps = relationship("Cap", back_populates="city")

    def to_dict(self):
        return {
            "istat_code": self.istat_code,
            "province_code": self.province_code,
            "name": self.name,
            "province": self.province.to_dict()
        }

    def __repr__(self):
        return f"City(istat_code={self.istat_code}, name={self.name}, province_code={self.province_code})"

    def __eq__(self, other):
        if not isinstance(other, City):
            return False

        return self.istat_code==other.istat_code

@event.listens_for(City.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    print("Adding default city data...")

    with open("data/cities.json", encoding="utf-8") as file:
        content = file.read()
    
    data = json.loads(content)

    connection.execute(
        City.__table__.insert(),
        [
            {
                "istat_code": city[0],
                "province_code": city[1],
                "name": city[2],
            }
            for city in data
        ]
    )