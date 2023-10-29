# implement factory pattern to create repository
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from repository.address import AddressRepo
from repository.blog import BlogRepo
from repository.category import CategoryRepo
from repository.product import ProductRepo
from repository.review import ReviewRepo
from repository.blog import ReviewBlogRepo


class RepositoryFactory:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    def get_product_repo(self) -> ProductRepo:
        return ProductRepo(self.db)
    
    def get_category_repo(self) -> CategoryRepo:
        return CategoryRepo(self.db)
    
    def get_review_repo(self) -> ReviewRepo:
        return ReviewRepo(self.db)
    
    def get_blog_repo(self) -> BlogRepo:
        return BlogRepo(self.db)
    
    def get_review_blog_repo(self) -> ReviewBlogRepo:
        return ReviewBlogRepo(self.db)
    
    def get_address_repo(self) -> AddressRepo:
        return AddressRepo(self.db)