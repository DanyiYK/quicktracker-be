from sqlalchemy import Column, ForeignKey, String, Float, Boolean

from persistence.db_config import Base


class Delivery(Base):
    __tablename__ = "delivery"

    tracking_code = Column(String, primary_key=True)
    
    courier_cf = Column(ForeignKey("courier.fiscal_code"), nullable=False)
    package_id = Column(ForeignKey("package.id"), nullable=False, unique=True)
    creator_id = Column(ForeignKey("admin.id"), nullable=False)
    city_id = Column(ForeignKey("city.cod_istat"), nullable=False)
    
    address = Column(String(500), nullable=False)
    sender = Column(String(500), nullable=False)
    recipient = Column(String(500), nullable=False)
    
    is_closed = Column(Boolean, nullable=False, default=False)
    

    def to_dict(self):
        return {
        }

    def __repr__(self):
        return f"Delivery(tracking_code={self.tracking_code}, courier_cf={self.courier_cf}, package_id={self.package_id}, creator_id={self.creator_id}, city_id={self.city_id}, address={self.address}, reciptient={self.recipient}, sender={self.sender}, is_closed={self.is_closed})"

    def __eq__(self, other):
        if not isinstance(other, Delivery):
            return False

        return self.id==other.id