from sqlalchemy import event, Column, String
from sqlalchemy.orm import relationship
from persistence.db_config import Base
import json


class Region(Base):
    __tablename__ = "region"

    istat_code = Column(String(2), primary_key=True)
    name = Column(String(100), nullable=False)

    provinces = relationship("Province", back_populates="region", order_by="asc(Province.name)")

    def to_dict(self):
        return {
            "istat_code": self.istat_code,
            "name": self.name
        }

    def __repr__(self):
        return f"Region(istat_code={self.istat_code}, name={self.name})"

    def __eq__(self, other):
        if not isinstance(other, Region):
            return False

        return self.istat_code==other.istat_code

@event.listens_for(Region.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    print("Adding default region data...")
    
    with open("data/regions.json") as file:
        content = file.read()
    
    data = json.loads(content)

    connection.execute(
        Region.__table__.insert(),
        [
            {
                "istat_code": region[0],
                "name": region[1],
            }
            for region in data
        ]
    )
