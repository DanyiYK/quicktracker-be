from sqlalchemy import event, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped
from persistence.db_config import Base
import json

class City(Base):
    __tablename__ = "city"

    cod_istat = Column(String(6), primary_key=True)
    province_istat = Column(ForeignKey("province.cod_istat"))
    name = Column(String(100), nullable=False)

    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)

    province: Mapped["Province"] = relationship()

    def to_dict(self):
        return {
            "cod_istat": self.cod_istat,
            "province_istat": self.province_istat,
            "name": self.name,
        }

    def __repr__(self):
        return f"City(cod_istat={self.cod_istat}, name={self.name}, province_istat={self.province_istat})"

    def __eq__(self, other):
        if not isinstance(other, City):
            return False

        return self.cod_istat==other.cod_istat

@event.listens_for(City.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    print("Adding default city data...")

    with open("data/cities.json") as file:
        content = file.read()
    
    data = json.loads(content)

    connection.execute(
        City.__table__.insert(),
        [
            {
                "cod_istat": city["cod_istat"],
                "province_istat": city["province_istat"],
                "name": city["name"],
                "lat": city["lat"],
                "long": city["long"]
            }
            for city in data
        ]
    )