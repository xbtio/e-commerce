from sqlalchemy import Time, Column, ForeignKey, Integer, String, Float, DateTime, MetaData
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db_config.db_connection import Base
from sqlalchemy.orm import backref

class OrderRequest(Base):  
    __tablename__ = 'order_requests'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_email: Mapped[str] = mapped_column(String(250), nullable=False)   
    name_of_recipient: Mapped[str] = mapped_column(String(150), nullable=False)
    phone_of_recipient: Mapped[str] = mapped_column(String(150), nullable=False)
    additional_num: Mapped[str] = mapped_column(String(150), nullable=False)
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('address.id'), nullable=False)
    order_weigth: Mapped[int] = mapped_column(Integer, nullable=False)
    order_status: Mapped[str] = mapped_column(String(150), default='pending', nullable=False)
    passport_series: Mapped[str] = mapped_column(String(4), nullable=True)
    passport_number: Mapped[str] = mapped_column(String(30), nullable=True)
    passport_date_of_issue: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    passport_organization: Mapped[str] = mapped_column(String(255), nullable=True)
    tin: Mapped[str] = mapped_column(String(12), nullable=True)

    address = relationship("Address", back_populates="order_request")
    product_for_order = relationship("ProductForOrder", back_populates="order_request", cascade="all, delete-orphan")

class ProductForOrder(Base):
    __tablename__ = 'product_for_order'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_request_id: Mapped[int] = mapped_column(Integer, ForeignKey('order_requests.id', ondelete='cascade'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id', ondelete='cascade'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order_request = relationship("OrderRequest", back_populates="product_for_order")
