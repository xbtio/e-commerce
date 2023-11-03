from sqlalchemy import Time, Column, ForeignKey, Integer, String, Float, Date, MetaData
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db_config.db_connection import Base

class Order(Base):
    __tablename__ = 'order'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    sdek_order_uuid: Mapped[str] = mapped_column(String(150), nullable=False)

    user = relationship("User", back_populates="order")

