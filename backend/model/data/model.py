from sqlalchemy import Time, Column, ForeignKey, Integer, String, Float, Date, MetaData
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db_config.db_connection import Base
from fastapi_users.db import SQLAlchemyBaseUserTable



class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    review = relationship("Review", back_populates="user")
    review_blog = relationship("ReviewBlog", back_populates="user")
    address = relationship("Address", back_populates="user")
    order = relationship("Order", back_populates="user")
    shopping_cart = relationship("ShoppingCart", back_populates="user")

