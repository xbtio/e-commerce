from sqlalchemy import Time, Column, ForeignKey, Integer, String, Float, Date, MetaData
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db_config.db_connection import Base


class Blog(Base):
    __tablename__ = 'blog'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    published: Mapped[Date] = mapped_column(Date, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    image: Mapped[str] = mapped_column(String(150), nullable=False)

    review = relationship("ReviewBlog", backref="blog", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Blog(title={self.title}, content={self.content}, date={self.date}, user_id={self.user_id})"
    

class ReviewBlog(Base):
    __tablename__ = 'review_blog'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_of_user: Mapped[str] = mapped_column(String(150), nullable=False)
    comment: Mapped[str] = mapped_column(String(500), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id', ondelete='cascade'), nullable=False)
    blog_id: Mapped[int] = mapped_column(Integer, ForeignKey('blog.id'), nullable=False)

    user = relationship("User", back_populates="review_blog")
    def __repr__(self):
        return f"ReviewBlog(content={self.content}, date={self.date}, user_id={self.user_id}, blog_id={self.blog_id})"