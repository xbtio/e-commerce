
from sqlalchemy import Time, Column, ForeignKey, Integer, String, Float, Date, MetaData
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db_config.db_connection import Base
from sqlalchemy.orm import backref



class Product(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(350), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id'))
    image: Mapped[str] = mapped_column(String(150), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    number_of_ratings: Mapped[int] = mapped_column(Integer, nullable=False)


    category = relationship("Category", backref="product")
    review = relationship("Review", backref="product", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(350), nullable=False)

    # product = relationship("Product", back_populates="category")




