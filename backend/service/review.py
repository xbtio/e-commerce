from model.data.model import User
from model.data.product import Product
from model.data.review import Review
from sqlalchemy import func
from repository.review import ReviewRepo
from repository.product import ProductRepo
from model.request.review import ReviewCreate, ReviewSchema
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import datetime



class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_review(self, product_id: int, current_user: User, review: ReviewCreate):
        try:
            product_repo = ProductRepo(self.db)
        
        
            review_repo = ReviewRepo(self.db)
            new_review = ReviewSchema(name_of_user = current_user.name, comment = review.comment, user_id=current_user.id, product_id=product_id, rating = review.rating)
            await review_repo.insert_review(new_review.model_dump())

            total_rating = await review_repo.get_total_rating(product_id)
            
            total_review = await review_repo.get_total_reviews(product_id)

            if total_rating is None:
                    total_rating = 0
            if total_review is None:
                    total_review = 0

            average_rating = total_rating / total_review
            number_of_ratings = await product_repo.get_product_by_id(product_id)
            if number_of_ratings is not None:
                number_of_ratings = number_of_ratings.number_of_ratings
            else:
                number_of_ratings = 0
            await product_repo.update_product(product_id, {'rating' : average_rating, 'number_of_ratings' : number_of_ratings + 1})
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def update_review(self, id: int, review: ReviewCreate):
        try:
            review_repo = ReviewRepo(self.db)
            if review is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
            await review_repo.update_review(id, {'comment': review.comment, 'rating': review.rating})
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def get_all_reviews(self):
        try:
            review_repo = ReviewRepo(self.db)
            result = await review_repo.get_all_reviews()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return result
    
    async def delete_review(self, id: int):
        try:
            review_repo = ReviewRepo(self.db)
            product_repo = ProductRepo(self.db)
            review = await review_repo.get_review_by_id(id)   
            if review is not None:         
                product_id = review.product_id
                current_average_rating = await product_repo.get_product_by_id(product_id)
                if current_average_rating is not None:
                    current_average_rating = current_average_rating.rating
                else:
                    current_average_rating = 0

                total_rating = await review_repo.get_total_rating(product_id)
                total_reviews = await review_repo.get_total_reviews(product_id)
                if total_rating is not None and total_reviews is not None:
                    new_average_rating = current_average_rating if total_reviews == 0 else total_rating / total_reviews
                else:
                    total_rating = 0
                    total_reviews = 0
                    new_average_rating = 0
                await product_repo.update_product(product_id, {'rating' : new_average_rating, 'number_of_ratings' : total_reviews - 1}) 

                await review_repo.delete_review(id)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True

        



        

