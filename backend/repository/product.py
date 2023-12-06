from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.product import Product, ProductDescription
from model.request.product_description import ProductDescriptionCreateSchema
from sqlalchemy import update, delete, select, insert
from model.data.product import ProductImage
from sqlalchemy.orm import joinedload, contains_eager, selectinload, aliased


class ProductRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_product(self, product: Dict, descriptions: List[Dict[str, Any]], product_images: List[Dict[str, Any]]):
        try:
            product_insert_stmt = insert(Product).values(**product).returning(Product.id)
            result = await self.db.execute(product_insert_stmt)
            await self.db.flush()  # Flush to make sure the product ID is available even if not committed yet.
            product_id = result.fetchone()
            product_id_value = product_id[0] if product_id else None

            # Only proceed to insert descriptions if a product ID was obtained
            if product_id_value is not None:
                for image in product_images:
                    image_insert_stmt = insert(ProductImage).values(product_id=product_id_value, **image)
                    await self.db.execute(image_insert_stmt)
                for description in descriptions:
                    description_insert_stmt = insert(ProductDescription).values(product_id=product_id_value, **description)
                    await self.db.execute(description_insert_stmt)
                await self.db.commit()  # Commit at the end to ensure all inserts are done in a single transaction
                return product_id_value

        except Exception as e:
            await self.db.rollback()  # Rollback in case of any error during the transaction
            print(f"Exception during product insertion: {e}")
            return None  # Return None or raise an HTTPException for REST context

        return None
    
    async def update_product(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(Product).where(Product.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True

    async def delete_product(self, id: int):
        try:
            await self.db.execute(delete(Product).where(Product.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_all_products(self):
        result = await self.db.execute(select(Product))
        return result.scalars().all()
    
    async def get_product_by_id(self, id: int):
        # get info about product_description and product_image joined with product
        result = await self.db.execute(select(Product).where(Product.id == id).options(selectinload(Product.product_description), selectinload(Product.product_image)))
        return result.scalars().one_or_none()
        