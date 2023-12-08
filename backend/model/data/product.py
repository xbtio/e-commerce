from turtle import title
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
    weigth: Mapped[int] = mapped_column(Integer, nullable=False)
    length: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    

    category = relationship("Category", backref="product")
    review = relationship("Review", backref="product", cascade="all, delete-orphan")
    product_description = relationship("ProductDescription", backref="product", cascade="all, delete-orphan")
    shopping_cart_item = relationship("ShoppingCartItem", backref="product", cascade="all, delete-orphan")
    product_for_order = relationship("ProductForOrder", backref="product", cascade="all, delete-orphan")
    product_image = relationship("ProductImage", backref="product", cascade="all, delete-orphan")


class ProductDescription(Base):
    __tablename__ = 'product_description'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id', ondelete='cascade'))
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(350), nullable=False)


class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(350), nullable=False)
    parent_category_id: Mapped[int] = mapped_column(Integer, ForeignKey('parent_category.id'))

    # product = relationship("Product", back_populates="category")

class ParentCategory(Base):
    __tablename__ = 'parent_category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    category = relationship("Category", backref="parent_category", cascade="all, delete-orphan")


class ProductImage(Base):
    __tablename__ = 'product_image'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id', ondelete='cascade'))
    image: Mapped[str] = mapped_column(String(150), nullable=False)

