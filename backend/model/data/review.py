from sqlalchemy import Time, Column, ForeignKey, Integer, String, Float, Date, MetaData
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db_config.db_connection import Base
from sqlalchemy.orm import backref




class Review(Base):
    __tablename__ = 'review'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_of_user: Mapped[str] = mapped_column(String(150), nullable=False)
    comment: Mapped[str] = mapped_column(String(550), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id', ondelete='cascade'), nullable=False)
    created_at: Mapped[Date] = mapped_column(Date, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    user = relationship("User", back_populates="review")
    # product = relationship("Product", backref=backref("review", cascade="all,delete"))