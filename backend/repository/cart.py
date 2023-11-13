from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.cart import ShoppingCart, ShoppingCartItem
from model.data.product import Product
from sqlalchemy import update, delete, select, insert
from sqlalchemy.orm import joinedload, contains_eager, selectinload

class ShoppingCartRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def get_or_create_cart(self, user_id: int) -> ShoppingCart:
        result = await self.db.execute(select(ShoppingCart).where(ShoppingCart.user_id == user_id))
        cart = result.scalars().one_or_none()
        if cart is None:
            # Insert the new ShoppingCart without using returning()
            new_cart = ShoppingCart(user_id=user_id)
            self.db.add(new_cart)
            await self.db.commit()

            # Retrieve the cart instance with the generated ID
            await self.db.refresh(new_cart)
            return new_cart

        return cart
    
    async def update_cart(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(ShoppingCart).where(ShoppingCart.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def delete_cart(self, id: int):
        try:
            await self.db.execute(delete(ShoppingCart).where(ShoppingCart.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_all_carts(self):
        result = await self.db.execute(select(ShoppingCart))
        return result.scalars().all()
    
    async def get_cart_info_by_user_id(self, user_id: int):
        query = (
            select(ShoppingCart)
            .options(selectinload(ShoppingCart.items).selectinload(ShoppingCartItem.product))
            .where(ShoppingCart.user_id == user_id)
        )
        result = await self.db.execute(query)
        cart = result.unique().scalars().one_or_none()
        return cart

class ShoppingCartItemRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_cart_item(self, cart_item: Dict):
        try:
            await self.db.execute(insert(ShoppingCartItem).values(**cart_item))  
            await self.db.commit()
        except Exception as e:
            print(f"Exception during cart item insertion: {e}")
            return False 
        return True

    async def update_cart_item(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(ShoppingCartItem).where(ShoppingCartItem.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def delete_cart_item(self, id: int):
        try:
            await self.db.execute(delete(ShoppingCartItem).where(ShoppingCartItem.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_cart_item_by_cart_id(self, id: int):
        result =  await self.db.execute(select(ShoppingCartItem).where(ShoppingCartItem.cart_id == id))
        return result.scalars().one_or_none()
    
    async def get_cart_item_by_id(self, id: int):
        result =  await self.db.execute(select(ShoppingCartItem).where(ShoppingCartItem.id == id))
        return result.scalars().one_or_none()
    
    async def get_all_cart_items(self):
        result = await self.db.execute(select(ShoppingCartItem))
        return result.scalars().all()
    
    async def get_cart_items_by_cart_id(self, id: int):
        result =  await self.db.execute(select(ShoppingCartItem).where(ShoppingCartItem.cart_id == id))
        return result.scalars().all()
    
    async def get_cart_items_by_product_id(self, id: int):
        result =  await self.db.execute(select(ShoppingCartItem).where(ShoppingCartItem.product_id == id))
        return result.scalars().all()
    
    async def get_cart_items_by_product_id_and_cart_id(self, product_id: int, cart_id: int):
        result =  await self.db.execute(select(ShoppingCartItem).where(ShoppingCartItem.product_id == product_id).where(ShoppingCartItem.cart_id == cart_id))
        return result.scalars().all()
    
   
