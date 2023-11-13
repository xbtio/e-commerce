from pydantic import BaseModel
from typing import Optional

'''class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship("User", back_populates="shopping_cart")

class ShoppingCartItem(Base):
    __tablename__ = 'shopping_cart_item'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shopping_cart_id: Mapped[int] = mapped_column(Integer, ForeignKey('shopping_cart.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    shopping_cart = relationship("ShoppingCart", back_populates="shopping_cart_item")
    product = relationship("Product", back_populates="shopping_cart_item")'''

class ShoppingCartItemCreateSchema(BaseModel):
    product_id: int
    quantity: int