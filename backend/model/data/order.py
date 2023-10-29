from sqlalchemy import Time, Column, ForeignKey, Integer, String, Float, Date, MetaData
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db_config.db_connection import Base


# class Address(Base):
#     __tablename__ = 'address'
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     address_line: Mapped[str] = mapped_column(String(550), nullable=False)
#     postal_code: Mapped[str] = mapped_column(String(50), nullable=False)

#     cartitem= relationship("CartItem", back_populates="address")

# class CartItem(Base):
#     __tablename__ = 'cart_item'
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     quantity: Mapped[int] = mapped_column(Integer, nullable=False)
#     product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
#     order_id: Mapped[int] = mapped_column(Integer, ForeignKey('order.id'), nullable=False)

#     product= relationship("Product", back_populates="cartitem")
#     order = relationship("Order", back_populates="cartitem")


# class Order(Base):
#     __tablename__ = 'order'
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     order_amount: Mapped[int] = mapped_column(Integer, nullable=False)
#     address: Mapped[int] = mapped_column(Integer, ForeignKey('address.id'), nullable=False)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
#     created_at: Mapped[Date] = mapped_column(Date, nullable=False)

#     user = relationship("User", back_populates="order")
#     address = relationship("Address", back_populates="cartitem")
#     cartitem = relationship("CartItem", back_populates="order")

