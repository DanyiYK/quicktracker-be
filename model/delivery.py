from sqlalchemy import Column, ForeignKey, func, String, Float, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship

from persistence.db_config import Base

class Delivery(Base):
    __tablename__ = "delivery"

    id = Column(Integer, primary_key=True)
    tracking_code = Column(String, unique=True)
    creation_date = Column(DateTime, nullable=False, server_default=func.now())
    is_closed = Column(Boolean, nullable=False, default=False)

    courier_id = Column(ForeignKey("courier.id"), nullable=False)
    package_id = Column(ForeignKey("package.id"), nullable=False, unique=True)

    recipient_name = Column(String(500), nullable=False)
    recipient_cap_id = Column(ForeignKey("cap.id"), nullable=False)
    recipient_city_id = Column(ForeignKey("city.istat_code"), nullable=False)
    recipient_address = Column(String(500), nullable=False)

    sender_name = Column(String(500), nullable=False)
    sender_cap_id = Column(ForeignKey("cap.id"), nullable=False)
    sender_city_id = Column(ForeignKey("city.istat_code"), nullable=False)
    sender_address = Column(String(500), nullable=False)

    courier = relationship("Courier", back_populates="deliveries")
    package = relationship("Package")
    sender_cap = relationship("Cap", foreign_keys=[sender_cap_id, sender_city_id])
    sender_city = relationship("City", foreign_keys=[sender_city_id])
    recipient_cap = relationship("Cap", foreign_keys=[recipient_cap_id, recipient_city_id])
    recipient_city = relationship("City", foreign_keys=[recipient_city_id])


    def to_dict(self):
        return {
            "id": self.id,
            "tracking_code": self.tracking_code,
            "creation_date": self.creation_date,
            "is_closed": self.is_closed,

            "courier_id": self.courier_id,
            # "package_id": self.package_id,
            
            "recipient_name": self.recipient_name,
            # "recipient_cap_id": self.recipient_cap_id,
            # "recipient_city_id": self.recipient_city_id,
            "recipient_address": self.recipient_address,

            "sender_name": self.sender_name,
            # "sender_cap_id": self.sender_cap_id,
            # "sender_city_id": self.sender_city_id,
            "sender_address": self.sender_address,

            "package": self.package.to_dict(),
            "sender_city": self.sender_city.to_dict(),
            "sender_cap": self.sender_cap.cap,
            "recipient_city": self.recipient_city.to_dict(),
            "recipient_cap": self.recipient_cap.cap
        }

    def __repr__(self):
        return f"Delivery(tracking_code={self.tracking_code}, courier_cf={self.courier_cf}, package_id={self.package_id}, creator_id={self.creator_id}, city_id={self.city_id}, address={self.address}, reciptient={self.recipient}, sender={self.sender}, is_closed={self.is_closed})"

    def __eq__(self, other):
        if not isinstance(other, Delivery):
            return False

        return self.id==other.id