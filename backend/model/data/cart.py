from sqlalchemy import Time, Column, ForeignKey, Integer, String, Float, Date, MetaData
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db_config.db_connection import Base

class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship("User", back_populates="shopping_cart")
    items = relationship("ShoppingCartItem", back_populates="shopping_cart")

class ShoppingCartItem(Base):
    __tablename__ = 'shopping_cart_item'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shopping_cart_id: Mapped[int] = mapped_column(Integer, ForeignKey('shopping_cart.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id', ondelete='cascade'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    shopping_cart = relationship("ShoppingCart", back_populates="items")
    